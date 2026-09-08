from domains.followup.followup_state import ProcessReplyState


def route_by_action(state: ProcessReplyState):
    return state["assessment"]["action"]