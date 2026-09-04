from domains.followup.followup_state import InitialFollowupState
from domains.followup.graphs.initial_followup_graph import initial_followup_graph


def main():
    # 0. define param
    input_state: InitialFollowupState = {
        "followup_id": "F001",
        "patient_id": "P001",
        "treatment_id": "T001",
        "patient_context": {
            "patient_name": "张女士",
            "treatment_type": "矫正",
            "treatment_date": "2026-09-01",
            "followup_day": 1,
            "doctor_name": "李医生"
        },
    }


    # 1. run graph
    result = initial_followup_graph.invoke(input_state)
    print("=== Initial Follow-up Result ===")
    print(result)
    print()
    print("=== Generated Message ===")
    print(result["initial_msg"])


if __name__ == '__main__':
    main()
