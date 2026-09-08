export type FollowupAction = "NORMAL" | "ASK_MORE" | "ESCALATE";

export const mockFollowup = {
  patient: {
    name: "杨女士",
    treatment: "种植术后",
    followupDay: "Day 1",
    doctor: "Dr. 李",
  },
  initialMessage:
    "杨女士您好，这里是诊所术后回访。想了解一下您今天的恢复情况，目前疼痛大概几分？现在还有没有出血、肿胀或发烧？",
  latestPatientMessage:
    "医生您好，我从昨晚开始一直很疼，现在大概 8 分。嘴里还有血，不是只有一点血丝。脸好像有点肿，但没有发烧。",
  extractedFeedback: {
    pain: "8/10",
    currentBleeding: "Yes",
    swelling: "Unknown",
    fever: "No",
  },
  action: "ESCALATE" as FollowupAction,
  matchedRules: ["HIGH_PAIN", "ACTIVE_BLEEDING"],
  missingFields: ["Swelling severity", "Bleeding duration"],
  suggestedReply:
    "杨女士您好，您目前疼痛较明显且仍有出血，需要尽快由医生进一步判断。请先用干净纱布持续咬紧出血处 30 分钟，不要频繁吐口水或漱口。我们会立即通知医生，请保持电话畅通。如出血持续增多、出现呼吸或吞咽困难，请立即前往急诊。",
};
