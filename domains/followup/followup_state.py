import operator
from enum import StrEnum
from typing import TypedDict, Optional, Literal, Annotated
from domains.followup.schemas.patient_context import PatientContext

"""
=======================  0. BaseState =========================
"""
class FollowupBaseState(TypedDict, total=False):
    followup_id: str
    patient_id: str
    patient_context: PatientContext
    treatment_id: str



"""
======================= 1. InitialFollowupState =======================
"""
class InitialFollowupState(FollowupBaseState, total=False):
    initial_msg: str



"""
=======================  2. ProcessReplyState ==========================
"""
# ---------------------- 2.1 Events -------------------
class EventType(StrEnum):
    MESSAGE_GENERATED = "MESSAGE_GENERATED"
    MESSAGE_DELIVERED = "MESSAGE_DELIVERED"
    ASSESSMENT_COMPLETED = "ASSESSMENT_COMPLETED"
    FOLLOWUP_VIEWED = "FOLLOWUP_VIEWED"
    OWNER_CHANGED = "OWNER_CHANGED"

class ActorRole(StrEnum):
    PATIENT = "patient"
    CONSULTANT = "consultant"
    DOCTOR = "doctor"
    AI = "ai"
    SYSTEM = "system"

class Action(StrEnum):
    NORMAL = "NORMAL"
    ASK_MORE = "ASK_MORE"
    ESCALATE = "ESCALATE"

class FollowupStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    WAITING_PATIENT = "WAITING_PATIENT"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"

class MessageEventData(TypedDict, total=False):
    actor_role: ActorRole
    actor_id: str       # optional
    actor_name: str     # optional
    target_role: ActorRole
    target_id: str      # optional = external_userid
    target_name: str    # optional
    content: str

class AssessmentEventData(TypedDict):
    actor_role: Literal["ai"]
    action: Action
    matched_rules: list[str]
    missing_fields: list[str]

class ViewedEventData(TypedDict):
    actor_role: Literal["consultant", "doctor"]
    actor_name: str

class OwnerChangedEventData(TypedDict):
    actor_role: Literal["consultant", "doctor", "system"]
    actor_name: str
    from_owner_role: Literal["consultant", "doctor"]
    from_owner_name: str
    to_owner_role: Literal["consultant", "doctor"]
    to_owner_name: str

EventData = MessageEventData | AssessmentEventData | ViewedEventData | OwnerChangedEventData

class FollowupEvent(TypedDict):
    event_type: EventType
    data: EventData
    timestamp: str


# ---------------------- 2.2 Current Snapshots -------------------
class FeedbackSnapshot(TypedDict, total=False):
    pain_score: Optional[int]
    current_bleeding: Optional[bool]
    recent_bleeding: Optional[bool]
    swelling: Optional[bool]
    fever: Optional[bool]

class AssessmentSnapshot(TypedDict, total=False):
    action: Action
    matched_rules: list[str]
    missing_fields: list[str]


# ---------------------- 2.3 ProcessReplyState -------------------
class ProcessReplyState(FollowupBaseState, total=False):
    # ============= current working data =================
    patient_reply: str
    next_reply: str
    doctor_notification: str

    # =============== current snapshot ====================
    followup_status: FollowupStatus
    current_owner_role: Literal["consultant", "doctor"]
    current_owner_name: str
    patient_feedback: FeedbackSnapshot
    assessment: AssessmentSnapshot

    # =============== audit history ==================
    events: Annotated[list[FollowupEvent], operator.add]

