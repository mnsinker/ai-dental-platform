from pydantic import BaseModel, Field


class PatientFeedback(BaseModel):
    pain_score: int | None = Field(default=None, ge=0, le=10)
    current_bleeding: bool | None = None
    recent_bleeding: bool | None = None
    swelling: bool | None = None
    fever: bool | None = None