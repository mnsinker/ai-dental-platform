from infra.llm import get_llm


def main():
    llm = get_llm("qwen")

    response = llm.invoke("请只回复四个字：连接成功")

    print(response.content)


if __name__ == "__main__":
    main()