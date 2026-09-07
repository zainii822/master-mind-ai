from src.state.research_state import ResearchState

def run_quality_control(state: ResearchState) -> dict:
    """
    Audits the research state for defect classes:
    - Coverage gaps (unanswered sub-questions)
    - Unsupported claims (evidence missing or unresolvable)
    Returns a QC verdict, defect list, and targeted gap questions.
    """
    state.current_stage = "quality_control"
    defects = []
    
    # 1. Check for coverage gaps (unanswered questions)
    for q_id, status in state.question_status.items():
        if status != "answered":
            defects.append({
                "defect_type": "CoverageGap",
                "severity": "high",
                "location": f"Question {q_id}",
                "gap_question": f"Need further investigation for sub-question {q_id}"
            })

    # 2. Check evidence binding
    for evidence in state.evidence_store:
        if not evidence.source_ref:
            defects.append({
                "defect_type": "UnsupportedClaim",
                "severity": "critical",
                "location": f"Evidence ID {evidence.evidence_id}",
                "gap_question": f"Provide valid source reference for claim: {evidence.claim}"
            })

    passed = len(defects) == 0
    verdict = {
        "passed": passed,
        "defect_count": len(defects),
        "defects": defects,
        "repair_questions": [d["gap_question"] for d in defects if "gap_question" in d]
    }
    
    state.defect_list.extend(defects)
    return verdict