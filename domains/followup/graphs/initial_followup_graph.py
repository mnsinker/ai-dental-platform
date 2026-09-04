from langgraph.graph import StateGraph, START, END
from domains.followup.followup_state import InitialFollowupState
from domains.followup.nodes.generate_initial_msg import generate_initial_msg

def build_initial_followup_graph():
    builder = StateGraph(InitialFollowupState)
    builder.add_node("generate_initial_msg", generate_initial_msg)

    builder.add_edge(START, "generate_initial_msg")
    builder.add_edge("generate_initial_msg", END)

    graph = builder.compile()
    return graph

initial_followup_graph = build_initial_followup_graph()

