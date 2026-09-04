from domains.followup.followup_state import ProcessReplyState
from domains.followup.policies.followup_fields import REQUIRED_FIELDS
from domains.followup.policies.followup_rules import RULES


def evaluate_policy(state: ProcessReplyState) -> dict:
    # case 1. ESCALATE
    matched_rules = [rule["rule_id"] for rule in RULES if rule["condition"](state)]
    if matched_rules:
        return {
            "action": "ESCALATE",
            "matched_rules": matched_rules,
            "missing_fields": [],
        }

    # case 2. ASK_MORE
    missing_fields = [field for field in REQUIRED_FIELDS if state.get(field) is None]
    if missing_fields:
        return {
            "action": "ASK_MORE",
            "matched_rules": ["MISSING_FIELDS"],
            "missing_fields": missing_fields,
        }

    # case 3. NORMAL
    return {
        "action": "NORMAL",
        "matched_rules": ["NORMAL_RECOVERY"],
        "missing_fields": [],
    }
