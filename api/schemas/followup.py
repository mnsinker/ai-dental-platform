from pydantic import BaseModel


class ReplyRequest(BaseModel):
    followup_id: str
    patient_id: str
    treatment_id: str
    patient_name: str
    patient_reply: str


class ReplyResponse(BaseModel):
    action: str | None = None
    matched_rules: list[str] = []
    missing_fields: list[str] = []
    next_reply: str | None = None
    doctor_notification: str | None = None

    pain_score: int | None = None
    current_bleeding: bool | None = None
    swelling: bool | None = None
    fever: bool | None = None