RULES = [
    {
        "rule_id": "HIGH_PAIN",
        "condition": lambda feedback: feedback.get("pain_score") is not None and feedback["pain_score"] >= 7,
        "action": "ESCALATE",
    },

    {
        "rule_id": "ACTIVE_BLEEDING",
        "condition": lambda feedback: feedback.get("current_bleeding") is True,
        "action": "ESCALATE",
    },

    {
        "rule_id": "FEVER",
        "condition": lambda feedback: feedback.get("fever") is True,
        "action": "ESCALATE",
    },
]

