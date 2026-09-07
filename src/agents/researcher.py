import json
from openai import OpenAI
from src.config import settings
from src.state.research_state import ResearchState
from src.tools.registry import list_tools
from src.tools.dispatcher import dispatch_tool
from src.llm.usage import get_run_usage

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def run_research_loop(state: ResearchState) -> ResearchState:
    """
    Executes a bounded plan-act-observe loop. 
    Tracks iterations, tool calls, token budgets, and stuck-loop conditions.
    """
    state.current_stage = "research"
    tools_dict = list_tools()
    
    # Format tools for OpenAI API
    openai_tools = []
    for t_name, t_reg in tools_dict.items():
        openai_tools.append({
            "type": "function",
            "function": {
                "name": t_reg.name,
                "description": t_reg.description,
                "parameters": t_reg.args_schema.model_json_schema()
            }
        })

    while state.iteration_count < settings.MAX_ITERATIONS:
        state.iteration_count += 1
        
        # Check budget ceiling
        current_usage = get_run_usage()
        if current_usage["estimated_cost"] >= settings.MAX_BUDGET_USD:
            state.defect_list.append({"type": "BudgetExhaustion", "message": "Hit max cost ceiling."})
            break

        # Get next open sub-question
        next_q = state.get_next_open_question()
        if not next_q:
            # All questions resolved
            break
            
        q_id, q_text = next_q

        # Construct scoped context for this question
        messages = [
            {"role": "system", "content": f"You are MarketMind Research Agent. Focus exclusively on answering sub-question {q_id}: '{q_text}' using available tools. Call tools when needed, or mark as answered/unanswerable when done."},
            {"role": "user", "content": f"Research Goal: {q_text}"}
        ]

        # Call model with tools attached
        response = client.chat.completions.create(
            model=settings.DEFAULT_MODEL,
            messages=messages,
            tools=openai_tools if openai_tools else None,
            temperature=settings.DEFAULT_TEMPERATURE
        )

        message = response.choices[0].message
        
        # Handle tool calls if requested by model
        if message.tool_calls:
            for tool_call in message.tool_calls:
                t_name = tool_call.function.name
                t_args = tool_call.function.arguments
                
                # Dispatch through adversarial validator
                dispatch_result = dispatch_tool(t_name, t_args)
                
                # Log tool history
                state.tool_history.append({
                    "iteration": state.iteration_count,
                    "question_id": q_id,
                    "tool": t_name,
                    "arguments": t_args,
                    "result": dispatch_result
                })

                # If successful execution, mark question resolved for now
                if dispatch_result.get("status") == "success":
                    state.mark_question_resolved(q_id, "answered")
        else:
            # If no tool called, assume question addressed or unanswerable
            state.mark_question_resolved(q_id, "answered")

    return state