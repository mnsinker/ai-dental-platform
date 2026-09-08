from domains.followup.nodes.extract_feedback import extract_feedback


state = {
    "patient_reply": "不疼"
}

result = extract_feedback(state)

print(result)