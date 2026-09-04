from pydantic import BaseModel
from infra.llm import llm_qwen


class TestOutput(BaseModel):
    pain_score: int | None = None
    fever: bool | None = None


structured_llm = llm_qwen.with_structured_output(TestOutput)

result = structured_llm.invoke(
    "患者说：现在疼痛3分，没有发烧。"
)

print(result)