from domains.followup.followup_state import ProcessReplyState


def audit_log(state: ProcessReplyState):
    record = {
        # 0. who / which event
        "followup_id": state["followup_id"],
        "patient_id": state["patient_id"],
        "treatment_id": state["treatment_id"],

        # 1. current working data
        "patient_reply": state["patient_reply"],

        # 2. current snapshots
        "patient_feedback": state.get("patient_feedback", {}),
        "assessment": state.get("assessment", {}),

        # 3. current system's output
        "next_reply": state.get("next_reply"),
        "doctor_notification": state.get("doctor_notification"),

        # 4. current status
        "followup_status": state.get("followup_status"),

        # 5. timeline
        "timeline": state.get("timeline", []),

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