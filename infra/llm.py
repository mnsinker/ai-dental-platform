from langchain_core.runnables.graph import Graph
from langchain_openai import ChatOpenAI
from core.config import settings


def get_llm(provider: str = "qwen") -> ChatOpenAI:
    if provider == "qwen":
        return ChatOpenAI(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_BASE_URL,
            model=settings.QWEN_MODEL,
            temperature=0.2,
            timeout=10,
            max_retries=1,
        )

    if provider == "deepseek":
        return ChatOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            model=settings.DEEPSEEK_MODEL,
            temperature=0.2,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")


llm_qwen = get_llm()