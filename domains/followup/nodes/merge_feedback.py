from domains.followup.followup_state import ProcessReplyState


def merge_feedback(state: ProcessReplyState) -> dict:
    last_feedback = state["last_feedback"]
    return {
        "pain_score": last_feedback["pain_score"] if last_feedback["pain_score"] is not None else state.get("pain_score"),
        "current_bleeding": last_feedback["current_bleeding"] if last_feedback["current_bleeding"] is not None else state.get("current_bleeding"),
        "recent_bleeding": last_feedback["recent_bleeding"] if last_feedback["recent_bleeding"] is not None else state.get("recent_bleeding"),
        "swelling": last_feedback["swelling"] if last_feedback["swelling"] is not None else state.get("swelling"),
        "fever": last_feedback["fever"] if last_feedback["fever"] is not None else state.get("fever"),
    }

