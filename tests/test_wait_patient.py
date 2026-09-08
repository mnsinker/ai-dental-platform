from langgraph.types import Command
from domains.followup.graphs.process_reply_graph import process_reply_graph



config = {"configurable": {"thread_id": "followup:F001"}}
result = process_reply_graph.invoke(
    {
        "followup_id": "F001",
        "patient_id": "P001",
        "treatment_id": "T001",
        "patient_context": {"patient_name": "王女士"},
        "patient_reply": "现在特别疼，大概8分，而且还在出血，没有发烧。",
    },
    config=config,
)
print(result)


