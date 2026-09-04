from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from domains.followup.followup_state import ProcessReplyState
from domains.followup.nodes.audit_log import audit_log
from domains.followup.nodes.extract_feedback import extract_feedback
from domains.followup.nodes.evaluate_policy import evaluate_policy
from domains.followup.nodes.generate_doctor_notification import generate_doctor_notification
from domains.followup.nodes.generate_escalation_reply import generate_escalation_reply
from domains.followup.nodes.generate_further_questions import generate_further_questions
from domains.followup.nodes.generate_normal_reply import generate_normal_reply
from domains.followup.nodes.merge_feedback import merge_feedback
from domains.followup.nodes.route_by_action import route_by_action
from domains.followup.nodes.send_notification_to_doctor import send_notification_to_doctor
from domains.followup.nodes.wait_patient import wait_patient


def build_process_reply_graph():
    builder = StateGraph(ProcessReplyState)

    # ⭐️ NODES ========================================
    builder.add_node("extract_feedback", extract_feedback)
    builder.add_node("merge_feedback", merge_feedback)
    builder.add_node("evaluate_policy", evaluate_policy)

    # path_nodes 1
    builder.add_node("generate_normal_reply", generate_normal_reply)
    # path_nodes 2
    builder.add_node("generate_escalation_reply", generate_escalation_reply)
    builder.add_node("generate_doctor_notification", generate_doctor_notification)
    builder.add_node("send_notification_to_doctor", send_notification_to_doctor)
    builder.add_node("audit_log", audit_log)
    # path_nodes 3
    builder.add_node("generate_further_questions", generate_further_questions)
    builder.add_node("wait_patient", wait_patient)

    # ⭐️ EDGES ========================================
    builder.add_edge(START, "extract_feedback")
    builder.add_edge("extract_feedback", "merge_feedback")
    builder.add_edge("merge_feedback", "evaluate_policy")

    # 🔹CONDITIONAL EDGES - START ==========
    builder.add_conditional_edges(
        "evaluate_policy",
        route_by_action,
        path_map={
            # left = return value from "route by action";
            # right = node name
            "NORMAL": "generate_normal_reply",
            "ESCALATE": "generate_escalation_reply",
            "ASK_MORE": "generate_further_questions",
        }
    )
    # 🔹CONDITIONAL EDGES - END =========

    # path 1-cont.
    builder.add_edge("generate_normal_reply", END)
    # path 2-cont.
    builder.add_edge("generate_escalation_reply", "generate_doctor_notification")
    builder.add_edge("generate_doctor_notification", "send_notification_to_doctor")
    builder.add_edge("send_notification_to_doctor", "audit_log")
    builder.add_edge("audit_log", END)
    # path 3-cont.
    builder.add_edge("generate_further_questions", "wait_patient")
    builder.add_edge("wait_patient", "extract_feedback")

    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    return graph


process_reply_graph = build_process_reply_graph()
# mermaid = process_reply_graph.get_graph().draw_mermaid()
# print(mermaid)
