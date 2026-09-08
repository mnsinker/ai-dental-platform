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
    }
    config = {"configurable": {"thread_id": request.thread_id}}

    # 2. invoke graph
    result = process_reply_graph.invoke(input_state, config=config)

    # 3. return values back to FE
    return {
        "followup_id": result.get("followup_id", request.followup_id),
        "patient_id": result.get("patient_id", request.patient_id),
        "treatment_id": result.get("treatment_id", request.treatment_id),
        "followup_status": result.get("followup_status"),
        "patient_feedback": result.get("patient_feedback", {}),
        "assessment": result.get("assessment", {}),
        "next_reply": result.get("next_reply"),
        "doctor_notification": result.get("doctor_notification"),
        "events": result.get("events", []),
    }


@router.get("/state/{thread_id}")
def get_followup_state(thread_id: str):
    config = {"configurable": {"thread_id": thread_id,}}

    snapshot = process_reply_graph.get_state(config)
    values = snapshot.values or {}

    return {
        "thread_id": thread_id,
        "followup_id": values.get("followup_id"),
        "events": values.get("events", []),
    }

