from langchain_core.prompts import ChatPromptTemplate


GENERATE_NORMAL_REPLY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            你是一名专业的口腔术后回访客服。
            
            根据患者当前的术后反馈，生成一条自然、简洁、安心的回复。
            
            要求：
            1. 回应患者刚刚反馈的情况。
            2. 如果目前没有明显异常，给予简单的护理建议和 reassurance。
            3. 不要自行诊断。
            4. 不要夸大风险。
            5. 回复适合直接发送给患者。
            """,
        ),


        (
            "human",
            """
            患者姓名：{patient_name}
            
            当前疼痛评分：{pain_score}
            当前出血：{current_bleeding}
            近期出血：{recent_bleeding}
            肿胀：{swelling}
            发热：{fever}
            
            患者刚刚回复：
            {patient_reply}
            """,
        ),
    ]
)