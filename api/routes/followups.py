from api.schemas.followup import ReplyRequest, ReplyResponse
from domains.followup.graphs.process_reply_graph import process_reply_graph
from fastapi import APIRouter

router = APIRouter(prefix="/followups", tags=["followups"])


@router.post("/reply", response_model=ReplyResponse)
def process_reply(request: ReplyRequest):
    # 1. prep params
    input_state = {
        "followup_id": request.followup_id,
        "patient_id": request.patient_id,
        "treatment_id": request.treatment_id,
        "patient_context": {"patient_name": request.patient_name},
        "patient_reply": request.patient_reply,
        "patient_reply_history": [request.patient_reply],
    }
    config = {"configurable": {"thread_id": f"followup:{request.followup_id}"}}

    # 2. invoke graph
    result = process_reply_graph.invoke(input_state, config=config)
    return {
        "action": result.get("action"),
        "matched_rules": result.get("matched_rules", []),
        "missing_fields": result.get("missing_fields", []),
        "next_reply": result.get("next_reply"),
        "doctor_notification": result.get("doctor_notification"),
        "pain_score": result.get("pain_score"),
        "current_bleeding": result.get("current_bleeding"),
        "swelling": result.get("swelling"),
        "fever": result.get("fever"),
    }

