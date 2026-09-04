import operator
from typing import TypedDict, Optional, Literal, Annotated
from domains.followup.schemas.patient_context import PatientContext

Action = Literal["NORMAL", "ASK_MORE", "ESCALATE"]

class FollowupBaseState(TypedDict, total=False):
    followup_id: str
    patient_id: str

    patient_context: PatientContext
    treatment_id: str



class InitialFollowupState(FollowupBaseState, total=False):
    initial_msg: str



class ProcessReplyState(FollowupBaseState, total=False):
    # 1. patient reply
    patient_reply: str
    patient_reply_history: Annotated[list[str], operator.add]


    # 2. feedback (extracted from reply)
    # 2.1 current feedback
    pain_score: Optional[int]
    current_bleeding: Optional[bool]
    recent_bleeding: Optional[bool]
    swelling: Optional[bool]
    fever: Optional[bool]
    # 2.2 last feedback
    last_feedback: Optional[dict]

    # 3. policy result
    action: Action
    matched_rules: list[str]
    missing_fields: list[str]

    # 4. 给咨询师的下一条建议话术
    next_reply: str

    # 5. doc notification
    doctor_notification: str

