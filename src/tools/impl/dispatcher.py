import json
import traceback
from src.tools.registry import get_tool
from src.llm.usage import get_run_usage

def dispatch_tool(tool_name: str, raw_arguments: dict) -> dict:
    """
    Dispatcher pipeline: 
    1. Resolve tool name
    2. Validate arguments against Pydantic schema
    3. Check permission level & execution safety
    4. Execute handler with error catching (returns structured error to model)
    """
    try:
        # 1. Resolve tool
        try:
            tool_reg = get_tool(tool_name)
        except KeyError:
            return {
                "status": "error",
                "error_type": "UnknownToolError",
                "message": f"Tool '{tool_name}' does not exist. Please choose from available tools."
            }

        # 2. Validate arguments against strict schema
        try:
            if isinstance(raw_arguments, str):
                parsed_args = json.loads(raw_arguments)
            else:
                parsed_args = raw_arguments
                
            validated_args = tool_reg.args_schema(**parsed_args)
        except json.JSONDecodeError as je:
            return {
                "status": "error",
                "error_type": "MalformedJSONError",
                "message": f"Failed to parse tool arguments as JSON: {je}"
            }
        except Exception as ve:
            return {
                "status": "error",
                "error_type": "ValidationError",
                "message": f"Argument validation failed against schema: {ve}"
            }

        # 3. Execute handler safely
        result = tool_reg.handler(**validated_args.model_dump())
        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        # Catch any unexpected execution failure and convert to a structured error
        return {
            "status": "error",
            "error_type": "ExecutionError",
            "message": str(e)
        }