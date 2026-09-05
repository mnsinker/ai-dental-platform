import hashlib
import secrets
import time
from integrations.wecom.client import get_agent_jsapi_ticket


def generate_js_sdk_signature(url: str) -> dict:
    ticket = get_agent_jsapi_ticket()

    timestamp = int(time.time())
    nonce_str = secrets.token_hex(8)

    sign_string = (
        f"jsapi_ticket={ticket}"
        f"&noncestr={nonce_str}"
        f"&timestamp={timestamp}"
        f"&url={url}"
    )

    signature = hashlib.sha1(sign_string.encode("utf-8")).hexdigest()

    return {
        "timestamp": timestamp,
        "nonce_str": nonce_str,
        "signature": signature,
    }