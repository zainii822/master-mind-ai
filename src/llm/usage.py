_RUN_USAGE = {"tokens_in": 0, "tokens_out": 0, "estimated_cost": 0.0}

def track_usage(stage: str, model: str, tokens_in: int, tokens_out: int):
    _RUN_USAGE["tokens_in"] += tokens_in
    _RUN_USAGE["tokens_out"] += tokens_out
    
    # Cost estimation per 1k tokens based on model tier
    if "mini" in model:
        cost = (tokens_in * 0.00015 / 1000) + (tokens_out * 0.0006 / 1000)
    else:
        cost = (tokens_in * 2.50 / 1000) + (tokens_out * 10.00 / 1000)
        
    _RUN_USAGE["estimated_cost"] += cost

def get_run_usage() -> dict:
    return _RUN_USAGE.copy()

def reset_usage():
    _RUN_USAGE["tokens_in"] = 0
    _RUN_USAGE["tokens_out"] = 0
    _RUN_USAGE["estimated_cost"] = 0.0