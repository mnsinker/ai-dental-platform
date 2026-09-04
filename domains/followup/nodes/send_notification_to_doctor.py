from domains.followup.followup_state import ProcessReplyState


def send_notification_to_doctor(state: ProcessReplyState):
    notification = state["doctor_notification"]
    # 后续真实实现：
    # wecom_client.send_internal_message(
    #     doctor_id=...,
    #     content=notification,
    # )
    return {}