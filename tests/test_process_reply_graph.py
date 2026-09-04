from domains.followup.graphs.process_reply_graph import build_process_reply_graph


def run_case(
    case_name: str,
    thread_id: str,
    patient_reply: str,
):
    graph = build_process_reply_graph()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {
            "followup_id": thread_id.split(":")[-1],
            "patient_id": "P001",
            "treatment_id": "T001",
            "patient_context": {
                "patient_name": "王女士"
            },
            "patient_reply": patient_reply,
            "patient_reply_history": [patient_reply],
        },
        config=config,
    )

    print(f"\n===== {case_name} =====")
    print("patient_reply:", patient_reply)
    print("action:", result.get("action"))
    print("matched_rules:", result.get("matched_rules"))
    print("missing_fields:", result.get("missing_fields"))
    print("next_reply:", result.get("next_reply"))
    print("doctor_notification:", result.get("doctor_notification"))
    print("interrupt:", result.get("__interrupt__"))

    return result


# =========================================================
# CASE 1: NORMAL
# =========================================================

normal_result = run_case(
    case_name="NORMAL",
    thread_id="followup:F_NORMAL",
    patient_reply="现在疼痛3分，没有出血，有一点肿，没有发烧。",
)

assert normal_result["action"] == "NORMAL"
assert normal_result["matched_rules"] == ["NORMAL_RECOVERY"]
assert normal_result["missing_fields"] == []
assert normal_result.get("next_reply")

print("NORMAL PASSED")


# =========================================================
# CASE 2: ASK_MORE
# =========================================================

ask_more_result = run_case(
    case_name="ASK_MORE",
    thread_id="followup:F_ASK_MORE",
    patient_reply="昨天还流血，今天已经不流了", #
)

assert ask_more_result["action"] == "ASK_MORE"
assert "MISSING_FIELDS" in ask_more_result["matched_rules"]
assert len(ask_more_result["missing_fields"]) > 0
assert ask_more_result.get("next_reply")
assert ask_more_result.get("__interrupt__")

print("ASK_MORE PASSED")


# =========================================================
# CASE 3: ESCALATE
# =========================================================

escalate_result = run_case(
    case_name="ESCALATE",
    thread_id="followup:F_ESCALATE",
    patient_reply="现在特别疼，大概8分，而且还在出血，没有发烧。",
)

assert escalate_result["action"] == "ESCALATE"

assert "HIGH_PAIN" in escalate_result["matched_rules"]
assert "ACTIVE_BLEEDING" in escalate_result["matched_rules"]

assert escalate_result["missing_fields"] == []
assert escalate_result.get("next_reply")
assert escalate_result.get("doctor_notification")

print("ESCALATE PASSED")


print("\n===== ALL 3 CASES PASSED =====")