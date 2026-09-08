from datetime import datetime, timezone
from domains.followup.followup_state import ActorRole, EventType, ProcessReplyState


def receive_patient_reply(state: ProcessReplyState) -> dict:
    patient_name = state.get("patient_context", {}).get("patient_name", "患者")
    consultant_name = state.get("current_owner_name", "张三咨询师")

    return {
        "events": [
            {
                "event_type": EventType.MESSAGE_DELIVERED.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "actor_role": ActorRole.PATIENT.value,
                    "actor_name": patient_name,
                    "target_role": ActorRole.CONSULTANT.value,
                    "target_name": consultant_name,
                    "content": state["patient_reply"],
                },
            }
        ]
    }