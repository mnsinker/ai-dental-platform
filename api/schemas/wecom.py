from pydantic import BaseModel


class WeComJsSdkSignatureResponse(BaseModel):
    corp_id: str
    agent_id: str
    timestamp: int
    nonce_str: str
    signature: str