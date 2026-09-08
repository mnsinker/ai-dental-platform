from domains.followup.followup_state import ProcessReplyState, EventType, ActorRole
from domains.followup.policies.followup_fields import REQUIRED_FIELDS
from domains.followup.policies.followup_rules import RULES
from datetime import datetime, timezone


def evaluate_policy(state: ProcessReplyState) -> dict:
    # 0. get current feedback
    feedback = state.get("patient_feedback")

    # case 1. ESCALATE
    matched_rules = [rule["rule_id"] for rule in RULES if rule["condition"](feedback)]
    if matched_rules:
        assessment = {
            "action": "ESCALATE",
            "matched_rules": matched_rules,
            "missing_fields": [],
        }

    # case 2. ASK_MORE
    else:
        missing_fields = [field for field in REQUIRED_FIELDS if feedback.get(field) is None]
        if missing_fields:
            assessment = {
                "action": "ASK_MORE",
                "matched_rules": ["MISSING_FIELDS"],
                "missing_fields": missing_fields,
            }

        # case 3. NORMAL
        else:
            assessment = {
                "action": "NORMAL",
                "matched_rules": ["NORMAL_RECOVERY"],
                "missing_fields": [],}


    return {
        "assessment": assessment,
        "events": [
            {
                "event_type": EventType.ASSESSMENT_COMPLETED.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "actor_role": ActorRole.AI.value,
                    "action": assessment["action"],
                    "matched_rules": assessment["matched_rules"],
                    "missing_fields": assessment["missing_fields"],
                }
            }
        ]
    }
