from pydantic import BaseModel


class WeComJsSdkSignatureResponse(BaseModel):
    corp_id: str
    agent_id: str
    timestamp: int
    nonce_str: str
    signature: str

class WeComDeliveredMessageRequest(BaseModel):
    followup_id: str
    thread_id: str
    actor_id: str | None = None
    actor_name: str | None = None
    target_id: str | None = None
    target_name: str | None = None
    content: str


class WeComDeliveredMessageResponse(BaseModel):
    followup_id: str
    event: dict