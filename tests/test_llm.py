from infra.llm import llm_qwen


response = llm_qwen.invoke("回复一句：测试成功")
print(response.content)