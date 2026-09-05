import requests
from core.config import settings

def get_access_token() -> str:
    response = requests.get(
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken",
        params={"corpid": settings.WECOM_CORP_ID, "corpsecret": settings.WECOM_SECRET},
        timeout=10,
    )

    data = response.json()
    if data.get("errcode") != 0:
        raise RuntimeError(f"WeCom gettoken failed: {data}")
    return data["access_token"]



def get_agent_jsapi_ticket() -> str:
    access_token = get_access_token()
    response = requests.get(
        "https://qyapi.weixin.qq.com/cgi-bin/ticket/get",
        params={"access_token": access_token, "type": "agent_config"},
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("errcode") != 0:
        raise RuntimeError(f"Failed to get WeCom agent jsapi ticket: {data}")

    return data["ticket"]