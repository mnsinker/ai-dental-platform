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
        },
        config=config,
    )

    print(f"\n===== {case_name} =====")
    print("patient_reply:", patient_reply)
    assessment = result.get("assessment", {})
    print("action:", assessment.get("action"))
    print("matched_rules:", assessment.get("matched_rules"))
    print("missing_fields:", assessment.get("missing_fields"))
    print("next_reply:", result.get("next_reply"))
    print("doctor_notification:", result.get("doctor_notification"))
    print("interrupt:", result.get("__interrupt__"))

    return result

# ============================================================================

def test_normal():
    result = run_case(
        case_name="NORMAL",
        thread_id="followup:F_NORMAL",
        patient_reply="现在疼痛3分，没有出血，有一点肿，没有发烧。",
    )

    assert result["assessment"]["action"] == "NORMAL"
    assert result["assessment"]["matched_rules"] == ["NORMAL_RECOVERY"]
    assert result["assessment"]["missing_fields"] == []
    assert result.get("next_reply")


def test_ask_more():
    result = run_case(
        case_name="ASK_MORE",
        thread_id="followup:F_ASK_MORE",
        patient_reply="昨天还流血，今天已经不流了",
    )

    assert result["assessment"]["action"] == "ASK_MORE"
    assert "MISSING_FIELDS" in result["assessment"]["matched_rules"]
    assert len(result["assessment"]["missing_fields"]) > 0
    assert result.get("next_reply")
    assert result.get("__interrupt__")


def test_escalate():
    result = run_case(
        case_name="ESCALATE",
        thread_id="followup:F_ESCALATE",
        patient_reply="现在特别疼，大概8分，而且还在出血，没有发烧。",
    )

    assert result["assessment"]["action"] == "ESCALATE"
    assert "HIGH_PAIN" in result["assessment"]["matched_rules"]
    assert "ACTIVE_BLEEDING" in result["assessment"]["matched_rules"]
    assert result["assessment"]["missing_fields"] == []
    assert result.get("next_reply")
    assert result.get("doctor_notification")