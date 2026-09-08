import json
from datetime import datetime, timezone

from ai.prompts.generate_further_questions import GENERATE_FURTHER_QUESTIONS_PROMPT
from domains.followup.followup_state import ProcessReplyState, EventType, ActorRole
from infra.llm import llm_qwen



def generate_further_questions(state: ProcessReplyState):
    # 1. prep prompt param

    # 1.1 prep: patient reply
    patient_reply = state.get("patient_reply", "")

    # 1.2 prep: patient feedback
    patient_feedback = state.get("patient_feedback", {})
    patient_feedback = json.dumps(patient_feedback, ensure_ascii=False)

    # 1.3 prep: assessment
    assessment = state.get("assessment", {})
    missing_fields = assessment.get("missing_fields", [])
    action = assessment.get("action")


    # 2. invoke llm
    chain = GENERATE_FURTHER_QUESTIONS_PROMPT | llm_qwen
    response = chain.invoke({
        "patient_reply": patient_reply,
        "feedback": patient_feedback,
        "action": action,
        "missing_fields": missing_fields,
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