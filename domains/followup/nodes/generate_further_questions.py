import json
from ai.prompts.generate_further_questions import GENERATE_FURTHER_QUESTIONS_PROMPT
from domains.followup.followup_state import ProcessReplyState
from infra.llm import llm_qwen



def generate_further_questions(state: ProcessReplyState):
    # 1. prep prompt param

    # 1.1 prep: patient reply
    patient_reply = state.get("patient_reply", "")

    # 1.2 prep: patient feedback
    patient_feedback = {
        "pain_score": state.get("pain_score"),
        "current_bleeding": state.get("current_bleeding"),
        "recent_bleeding": state.get("recent_bleeding"),
        "swelling": state.get("swelling"),
        "fever": state.get("fever"),
    }
    patient_feedback = json.dumps(patient_feedback, ensure_ascii=False)

    # 1.3 prep: missing_fields
    missing_fields = state["missing_fields"]

    # 1.4 prep: action
    action = state["action"]


    # 2. invoke llm
    chain = GENERATE_FURTHER_QUESTIONS_PROMPT | llm_qwen
    response = chain.invoke({
        "patient_reply": patient_reply,
        "feedback": patient_feedback,
        "action": action,
        "missing_fields": missing_fields,
    })

    return {"next_reply": response.content}