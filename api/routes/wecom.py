import os
from fastapi import APIRouter, Query
from api.schemas.wecom import WeComJsSdkSignatureResponse
from integrations.wecom.js_sdk import generate_js_sdk_signature


router = APIRouter(prefix="/wecom", tags=["wecom"])


@router.get("/js-sdk-signature", response_model=WeComJsSdkSignatureResponse)
def get_js_sdk_signature(url: str = Query(...)):
    signature_data = generate_js_sdk_signature(url)

    return {
        "corp_id": os.environ["WECOM_CORP_ID"],
        "agent_id": os.environ["WECOM_AGENT_ID"],
        **signature_data,
    }