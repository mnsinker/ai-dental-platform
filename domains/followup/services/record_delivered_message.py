from datetime import datetime, timezone

from domains.followup.followup_state import ActorRole, EventType
from domains.followup.graphs.process_reply_graph import process_reply_graph


def record_delivered_message(
    thread_id: str,
    content: str,
    actor_id: str | None = None,
    actor_name: str | None = None,
    target_id: str | None = None,
    target_name: str | None = None,
) -> dict:

    data = {
        "actor_role": ActorRole.CONSULTANT.value,
        "target_role": ActorRole.PATIENT.value,
        "content": content,
    }

    if actor_id:
        data["actor_id"] = actor_id
    if actor_name:
        data["actor_name"] = actor_name
    if target_id:
        data["target_id"] = target_id
    if target_name:
        data["target_name"] = target_name

    event = {
        "event_type": EventType.MESSAGE_DELIVERED.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }

    config = {"configurable": {"thread_id": thread_id,}}
    process_reply_graph.update_state(config, {"events": [event]},)
    return event