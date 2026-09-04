from domains.followup.followup_state import ProcessReplyState


def generate_doctor_notification(state: ProcessReplyState):
    patient_name = state["patient_context"]["patient_name"]
    patient_id = state["patient_id"]

    message = f"""
    异常提醒-术后回访
    患者姓名: {patient_name}
    患者ID: {patient_id}
    
    患者原始回复: 
    {state["patient_reply"]}
    
    结构化信息: 
    - 疼痛评分: {state.get("pain_score")}
    - 当前出血: {state.get("current_bleeding")}
    - 近期出血: {state.get("recent_bleeding")}
    - 肿胀: {state.get("swelling")}
    - 发热: {state.get("fever")}
    
    系统判断: ESCALATE
    """.strip()

    return {"doctor_notification": message}
