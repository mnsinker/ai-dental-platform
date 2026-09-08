from datetime import datetime, timezone

from ai.prompts.generate_escalation import GENERATE_ESCALATION_PROMPT
from domains.followup.followup_state import ProcessReplyState, EventType, ActorRole
from infra.llm import llm_qwen


def generate_escalation_reply(state: ProcessReplyState):
    chain = GENERATE_ESCALATION_PROMPT | llm_qwen
    patient_feedback = state.get("patient_feedback", {})

    response = chain.invoke({
        "patient_name": state["patient_context"]["patient_name"],
        "pain_score": patient_feedback.get("pain_score"),
        "current_bleeding": patient_feedback.get("current_bleeding"),
        "recent_bleeding": patient_feedback.get("recent_bleeding"),
        "swelling": patient_feedback.get("swelling"),
        "fever": patient_feedback.get("fever"),
        "patient_reply": state["patient_reply"],
    })

    return {
        "next_reply": response.content,
        "events": [
            {
                "event_type": EventType.MESSAGE_GENERATED.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "actor_role": ActorRole.AI.value,
                    "target_role": ActorRole.CONSULTANT.value,
                    "content": response.content,
                },
            }
        ],
    }
