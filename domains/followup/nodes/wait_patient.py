from langgraph.types import interrupt
from domains.followup.followup_state import ProcessReplyState


def wait_patient(state: ProcessReplyState):
    new_reply = interrupt(
        {
            "type": "WAIT_PATIENT_REPLY",
            "followup_id": state["followup_id"],
        }
    )

    return {
        "patient_reply": new_reply,
        "patient_reply_history": [new_reply],
    }