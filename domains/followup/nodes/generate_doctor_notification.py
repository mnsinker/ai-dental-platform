from domains.followup.followup_state import ProcessReplyState


def generate_doctor_notification(state: ProcessReplyState):
    patient_name = state["patient_context"]["patient_name"]
    patient_id = state["patient_id"]
    patient_feedback = state.get("patient_feedback", {})
    assessment = state.get("assessment", {})

    message = f"""
    异常提醒-术后回访
    患者姓名: {patient_name}
    患者ID: {patient_id}
    
    患者原始回复: 
    {state["patient_reply"]}
    
    结构化信息: 
    - 疼痛评分: {patient_feedback.get("pain_score")}
    - 当前出血: {patient_feedback.get("current_bleeding")}
    - 近期出血: {patient_feedback.get("recent_bleeding")}
    - 肿胀: {patient_feedback.get("swelling")}
    - 发热: {patient_feedback.get("fever")}
    
    系统判断: {assessment.get("action")}
    命中规则: {assessment.get("matched_rules", [])}
    """

    return {"doctor_notification": message}
