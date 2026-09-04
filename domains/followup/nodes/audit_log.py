from domains.followup.followup_state import ProcessReplyState


def audit_log(state: ProcessReplyState):
    record = {
        # 0. who / which event
        "followup_id": state["followup_id"],
        "patient_id": state["patient_id"],
        "treatment_id": state["treatment_id"],

        # 1.1 input
        "patient_reply": state["patient_reply"],
        # 1.2 system's understanding
        "feedback": {
            "pain_score": state.get("pain_score"),
            "current_bleeding": state.get("current_bleeding"),
            "recent_bleeding": state.get("recent_bleeding"),
            "swelling": state.get("swelling"),
            "fever": state.get("fever"),
        },

        # 2. decision
        "action": state["action"],
        "matched_rules": state.get("matched_rules"),
        "missing_fields": state.get("missing_fields"),

        # 3. system's output
        "next_reply": state.get("next_reply"),
        "doctor_notification": state.get("doctor_notification"),

        # # 4. execution result
        # "doctor_notification_status": "SENT",
        #
        # # 5. time
        # "created_at": "..."
    }
    # POC
    print(record)

    # Production:
    # audit_repository.save(record)

    return {} # 第一版 print() 就够了