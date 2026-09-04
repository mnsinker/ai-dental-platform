from langchain_core.prompts import ChatPromptTemplate

EXTRACT_FEEDBACK_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        你是口腔诊所术后回访的信息提取器。
        
        请只提取患者明确表达的信息，不要根据常识补全或猜测。
        
        规则：
        1. 如果某项信息没有明确提及，返回 null。
        2. 注意区分当前状态和之前发生过的状态。
        3. pain_score 只有患者明确给出 0-10 数字时才填写，否则返回 null。
        """,
        ),

        # example 1
        ("human", "患者回复：昨天有点出血，现在已经没有了。"),
        (
            "assistant",
            """{{
            "pain_score": null,
            "current_bleeding": false,
            "recent_bleeding": true,
            "swelling": null,
            "fever": null
            }}"""
        ),

        # example 2
        ("human", "患者回复：从昨天到现在一直都有一点出血。"),
        (
            "assistant",
            """{{            
              "pain_score": null,            
              "current_bleeding": true,            
              "recent_bleeding": true,            
              "swelling": null,            
              "fever": null            
            }}"""
        ),

        # example 3
        ( "human","患者回复：一直都没有出血。"),
        (
            "assistant",
            """{{
              "pain_score": null,        
              "current_bleeding": false,        
              "recent_bleeding": false,        
              "swelling": null,        
              "fever": null        
            }}""",
        ),

        # runtime input
        (
            "human", "患者回复: \n{patient_reply}"
        )


    ]
)