from pydantic import BaseModel


class ReplyRequest(BaseModel):
    thread_id: str
    followup_id: str
    patient_id: str
    treatment_id: str
    patient_name: str
    patient_reply: str


class ReplyResponse(BaseModel):
    followup_id: str
    patient_id: str
    treatment_id: str

    followup_status: str | None = None

    patient_feedback: dict = {}
    assessment: dict = {}

    next_reply: str | None = None
    doctor_notification: str | None = None

    timeline: list[dict] = []

