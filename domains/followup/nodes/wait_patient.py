from langgraph.types import interrupt
from domains.followup.followup_state import ActorRole, EventType, ProcessReplyState
from datetime import datetime, timezone


def wait_patient(state: ProcessReplyState):
    new_reply = interrupt(
        {
            "type": "WAIT_PATIENT_REPLY",
            "followup_id": state["followup_id"],
        }
    )

    patient_name = state.get("patient_context", {}).get("patient_name", "患者")
    consultant_name = state.get("current_owner_name", "咨询师")

    return {"patient_reply": new_reply}