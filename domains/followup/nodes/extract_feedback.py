from ai.prompts.extract_feedback import EXTRACT_FEEDBACK_PROMPT
from domains.followup.followup_state import ProcessReplyState
from domains.followup.schemas.patient_feedback import PatientFeedback
from infra.llm import llm_qwen




def extract_feedback(state: ProcessReplyState) -> dict:
    structured_llm = llm_qwen.with_structured_output(PatientFeedback)
    chain = EXTRACT_FEEDBACK_PROMPT | structured_llm
    patient_feedback = chain.invoke({"patient_reply": state["patient_reply"]})

    return {"last_feedback": patient_feedback.model_dump()}