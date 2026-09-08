from ai.prompts.extract_feedback import EXTRACT_FEEDBACK_PROMPT
from domains.followup.followup_state import ProcessReplyState
from domains.followup.schemas.patient_feedback import PatientFeedback
from infra.llm import llm_qwen




def extract_feedback(state: ProcessReplyState) -> dict:
    # 1. last feedback
    last_feedback = state.get("patient_feedback", {})

    # 2. new feedback
    structured_llm = llm_qwen.with_structured_output(PatientFeedback)
    chain = EXTRACT_FEEDBACK_PROMPT | structured_llm
    new_feedback = chain.invoke({"patient_reply": state["patient_reply"]}).model_dump()

    # 3. merged feedback
    merged_feedback = {
        key: value if value is not None else last_feedback.get(key)
        for key, value in new_feedback.items()
    }

    return {"patient_feedback": merged_feedback}

