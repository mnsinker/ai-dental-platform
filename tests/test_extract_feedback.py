from domains.followup.nodes.extract_feedback import extract_feedback


state = {
    "patient_reply": "昨天有点出血，现在已经没有了。"
}

result = extract_feedback(state)

print(result)