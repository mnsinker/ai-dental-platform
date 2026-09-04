from ai.prompts.generate_normal_reply import GENERATE_NORMAL_REPLY_PROMPT
from domains.followup.followup_state import ProcessReplyState
from infra.llm import llm_qwen


def generate_normal_reply(state: ProcessReplyState):
    chain = GENERATE_NORMAL_REPLY_PROMPT | llm_qwen
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
