import json
from openai import OpenAI
from src.config import settings
from src.schemas.plan import ResearchPlan

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PLANNER_SYSTEM_PROMPT = """You are an expert Research Planner for Verity Strategy Partners. 
Your job is to take a normalized business research request, identify objectives, and break them down into rigorous, answerable sub-questions. 
Every sub-question must be answerable through bounded tools and assigned specific evidence types and candidate tools. Avoid vague questions."""

def generate_research_plan(scope_description: str) -> ResearchPlan:
    """Generates a schema-validated ResearchPlan using OpenAI structured outputs."""
    response = client.beta.chat.completions.parse(
        model=settings.PLANNING_MODEL,
        temperature=settings.DEFAULT_TEMPERATURE,
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a comprehensive research plan for the following scope:\n\n{scope_description}"}
        ],
        response_format=ResearchPlan,
        timeout=settings.REQUEST_TIMEOUT
    )
    
    return response.choices[0].message.parsed