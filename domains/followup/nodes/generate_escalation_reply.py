from ai.prompts.generate_escalation import GENERATE_ESCALATION_PROMPT
from domains.followup.followup_state import ProcessReplyState
from infra.llm import llm_qwen


def generate_escalation_reply(state: ProcessReplyState):
    chain = GENERATE_ESCALATION_PROMPT | llm_qwen
    response = chain.invoke({
        "patient_name": state["patient_context"]["patient_name"],
        "pain_score": state.get("pain_score"),
        "current_bleeding": state.get("current_bleeding"),
        "recent_bleeding": state.get("recent_bleeding"),
        "swelling": state.get("swelling"),
        "fever": state.get("fever"),
        "patient_reply": state["patient_reply"],
    })
    return {"next_reply": response.content}
