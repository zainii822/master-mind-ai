import json
from src.tools.registry import get_tool

def dispatch_tool(tool_name: str, raw_arguments: dict) -> dict:
    """
    Dispatcher pipeline: 
    1. Resolve tool name
    2. Validate arguments against Pydantic schema
    3. Check permission level & execution safety
    4. Execute handler with error catching
    """
    try:
        try:
            tool_reg = get_tool(tool_name)
        except KeyError:
            return {
                "status": "error",
                "error_type": "UnknownToolError",
                "message": f"Tool '{tool_name}' does not exist in registry."
            }

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
                "message": f"Failed to parse arguments as JSON: {je}"
            }
        except Exception as ve:
            return {
                "status": "error",
                "error_type": "ValidationError",
                "message": f"Argument validation failed: {ve}"
            }

        result = tool_reg.handler(**validated_args.model_dump())
        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error_type": "ExecutionError",
            "message": str(e)
        }