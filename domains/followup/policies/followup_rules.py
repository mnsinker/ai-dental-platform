RULES = [
    {
        "rule_id": "HIGH_PAIN",
        "condition": lambda state: state.get("pain_score") is not None and state["pain_score"] >= 7,
        "action": "ESCALATE",
    },

    {
        "rule_id": "ACTIVE_BLEEDING",
        "condition": lambda state: state.get("current_bleeding") is True,
        "action": "ESCALATE",
    },

    {
        "rule_id": "FEVER",
        "condition": lambda state: state.get("fever") is True,
        "action": "ESCALATE",
    },
]

