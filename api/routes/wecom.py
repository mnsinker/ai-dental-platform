import os
from urllib.parse import urlencode
from fastapi import APIRouter, Query
from api.schemas.wecom import WeComJsSdkSignatureResponse, WeComDeliveredMessageResponse, WeComDeliveredMessageRequest
from domains.followup.services.record_delivered_message import record_delivered_message
from integrations.wecom.js_sdk import generate_js_sdk_signature
from integrations.wecom.client import get_user_id_by_code

router = APIRouter(prefix="/wecom", tags=["wecom"])


@router.get("/js-sdk-signature", response_model=WeComJsSdkSignatureResponse)
def get_js_sdk_signature(url: str = Query(...)):
    signature_data = generate_js_sdk_signature(url)

    return {
        "corp_id": os.environ["WECOM_CORP_ID"],
        "agent_id": os.environ["WECOM_AGENT_ID"],
        **signature_data,
    }


@router.get("/oauth/authorize-url")
def get_wecom_authorize_url(redirect_uri: str = Query(...)):
    query = urlencode(
        {
            "appid": os.environ["WECOM_CORP_ID"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "snsapi_base",
            "state": "dental-followup",
        }
    )

    return {"authorize_url": f"https://open.weixin.qq.com/connect/oauth2/authorize?{query}#wechat_redirect"}


@router.get("/oauth/user")
def get_wecom_user(code: str = Query(...)):
    user_id = get_user_id_by_code(code)
    return {"user_id": user_id}


@router.post("/messages/delivered", response_model=WeComDeliveredMessageResponse)
def record_wecom_delivered_message(request: WeComDeliveredMessageRequest):
    event = record_delivered_message(
        thread_id=request.thread_id,
        actor_id=request.actor_id,
        actor_name=request.actor_name,
        target_id=request.target_id,
        target_name=request.target_name,
        content=request.content,
    )

    return {
        "followup_id": request.followup_id,
        "event": event,
    }