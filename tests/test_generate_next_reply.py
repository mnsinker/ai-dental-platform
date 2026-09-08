from domains.followup.nodes.generate_further_questions import generate_further_questions
from domains.followup.followup_state import ProcessReplyState


def main():
    cases: list[ProcessReplyState] = [
        {
            "patient_reply": "今天大概疼3分，没有出血，有一点肿，没有发烧。",
            "pain_score": 3,
            "current_bleeding": False,
            "recent_bleeding": None,
            "swelling": True,
            "fever": False,
            "action": "NORMAL",
        },
        {
            "patient_reply": "有点疼，昨天晚上渗了一点血，不过今天好多了，没有发烧。",
            "pain_score": None,
            "current_bleeding": False,
            "recent_bleeding": True,
            "swelling": None,
            "fever": False,
            "action": "ASK_MORE",
        },
        {
            "patient_reply": "特别疼，大概8分，现在还一直出血，而且感觉有点发烧。",
            "pain_score": 8,
            "current_bleeding": True,
            "recent_bleeding": None,
            "swelling": None,
            "fever": True,
            "action": "ESCALATE",
        },
    ]

    for state in cases:
        result = generate_further_questions(state)

        print("=" * 50)
        print("Action:", state["assessment"]["action"])
        print("Reply:")
        print(result["next_reply"])


if __name__ == "__main__":
    main()