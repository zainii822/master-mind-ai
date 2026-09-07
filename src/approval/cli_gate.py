def render_approval_gate(state: dict, qc_verdict: dict) -> str:
    """
    Simulates the human approval decision interface.
    Supported outcomes: approve, reject, expand, rescope.
    """
    print("\n" + "="*50)
    print("🛡️ HUMAN APPROVAL GATE - MARKETMIND AI")
    print("="*50)
    print(f"Run ID: {state.get('run_id')}")
    print(f"QC Passed: {qc_verdict.get('passed')}")
    print(f"Outstanding Defects: {qc_verdict.get('defect_count')}")
    print("\nOptions: [1] Approve [2] Reject [3] Request Additional Research [4] Modify Scope")
    
    # For Streamlit / programmatic handling, we return a structured decision handler
    return "pending_human_input"