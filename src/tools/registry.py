from typing import Callable, Dict, Any, Type
from pydantic import BaseModel

class ToolRegistration(BaseModel):
    name: str
    description: str
    args_schema: Type[BaseModel]
    permission_level: str  # "read", "compute", "write"
    handler: Callable

_TOOL_REGISTRY: Dict[str, ToolRegistration] = {}

def register_tool(name: str, description: str, args_schema: Type[BaseModel], permission_level: str):
    def decorator(func: Callable):
        _TOOL_REGISTRY[name] = ToolRegistration(
            name=name,
            description=description,
            args_schema=args_schema,
            permission_level=permission_level,
            handler=func
        )
        return func
    return decorator

def get_tool(name: str) -> ToolRegistration:
    if name not in _TOOL_REGISTRY:
        raise KeyError(f"Tool '{name}' not found in registry.")
    return _TOOL_REGISTRY[name]

def list_tools() -> Dict[str, ToolRegistration]:
    return _TOOL_REGISTRY.copy()