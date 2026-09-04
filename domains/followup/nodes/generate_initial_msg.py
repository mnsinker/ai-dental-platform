from ai.prompts.followup import INITIAL_MESSAGE_PROMPT
from domains.followup.followup_state import InitialFollowupState
from infra.llm import llm_qwen

def generate_initial_msg(state: InitialFollowupState):
    # mock msg, to be replaced with llm later
    chain = INITIAL_MESSAGE_PROMPT | llm_qwen
    response = chain.invoke({"patient_context": state["patient_context"]})
    return {"initial_msg": response.content}
