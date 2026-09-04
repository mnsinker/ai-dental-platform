from domains.followup.nodes.evaluate_policy import evaluate_policy


def main():
    cases = [
        {
            "name": "NORMAL",
            "state": {
                "pain_score": 3,
                "current_bleeding": False,
                "swelling": True,
                "fever": False,
            },
            "expected": "NORMAL",
         },

        {
            "name": "ASK_MORE",
            "state": {
                "pain_score": None,
                "current_bleeding": False,
                "swelling": None,
                "fever": False,
            },
            "expected": "ASK_MORE",
        },

        {
            "name": "ESCALATE",
            "state": {
                "pain_score": 8,
                "current_bleeding": True,
                "swelling": None,
                "fever": True,
            },
            "expected": "ESCALATE",
        }
    ]

    for case in cases:
        result = evaluate_policy(case["state"])
        actual = result["action"]
        print(f"{case['name']}: {actual}")
        assert actual == case["expected"]

    print("All tests passed")

if __name__ == '__main__':
    main()