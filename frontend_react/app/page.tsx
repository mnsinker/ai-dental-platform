"use client";

import { useState } from "react";
import { mockFollowup } from "../data/mockFollowup";

const feedbackLabels = { pain: "疼痛", currentBleeding: "当前出血", swelling: "肿胀", fever: "发烧" } as const;
type Action = "NORMAL" | "ASK_MORE" | "ESCALATE";
type FollowupEvent = {
  event_type: string;
  timestamp: string;
  data: {
    actor_role?: string;
    actor_name?: string;
    target_role?: string;
    target_name?: string;
    content?: string;
    [key: string]: unknown;
  };
};

type ReplyResponse = {
  followup_id: string;
  patient_id: string;
  treatment_id: string;
  followup_status: string | null;

  patient_feedback: {
    pain_score: number | null;
    current_bleeding: boolean | null;
    recent_bleeding?: boolean | null;
    swelling: boolean | null;
    fever: boolean | null;
  };

  assessment: {
    action: Action | null;
    matched_rules: string[];
    missing_fields: string[];
  };

  next_reply: string | null;
  doctor_notification: string | null;

  events: FollowupEvent[];
};
type Stage = "initial" | "waiting" | "review" | "complete" | "escalated";

function yesNoUnknown(value: boolean | null) {
  return value === null ? "未知" : value ? "是" : "否";
}

export default function Home() {
  const [threadId] = useState(() => crypto.randomUUID());
  const consultantUserId = "consultant_001";
  const [stage, setStage] = useState<Stage>("initial");
  const [initialMessage, setInitialMessage] = useState(mockFollowup.initialMessage);
  const [patientReply, setPatientReply] = useState("");
  const [suggestedReply, setSuggestedReply] = useState("");
  const [events, setEvents] = useState<FollowupEvent[]>([]);
  const [result, setResult] = useState<ReplyResponse | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [copied, setCopied] = useState<"initial" | "suggested" | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);


  const feedback = result ? {
  pain: result.patient_feedback.pain_score == null
    ? "未知"
    : `${result.patient_feedback.pain_score}/10`,
  currentBleeding: yesNoUnknown(result.patient_feedback.current_bleeding),
  swelling: yesNoUnknown(result.patient_feedback.swelling),
  fever: yesNoUnknown(result.patient_feedback.fever),
} : null;

  async function copyText(text: string, target: "initial" | "suggested") {
    await navigator.clipboard.writeText(text);
    setCopied(target);
    window.setTimeout(() => setCopied(null), 1600);
  }

  async function refreshEvents() {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/followups/state/${threadId}`
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`${response.status} ${errorText}`);
  }

  const data: { events?: FollowupEvent[] } = await response.json();
  setEvents(data.events ?? []);
}

async function sendInitial() {
  const content = initialMessage.trim();
  if (!content || loading) return;

  setLoading(true);
  setError(null);

  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/wecom/messages/delivered`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          followup_id: "F001",
          thread_id: threadId,
          actor_id: consultantUserId ?? "consultant_001",
          actor_name: "张三咨询师",
          target_id: "patient_001",
          target_name: mockFollowup.patient.name,
          content,
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`${response.status} ${errorText}`);
    }

    await response.json();
    await refreshEvents();
    setStage("waiting");
  } catch (error) {
    setError(
      error instanceof Error
        ? `发送失败：${error.message}`
        : "发送失败，请稍后重试。"
    );
  } finally {
    setLoading(false);
  }
}

  async function handleAnalyze() {
    const content = patientReply.trim();
    if (!content || loading) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/followups/reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ followup_id: "F001", thread_id: threadId, patient_id: "P001", treatment_id: "T001", patient_name: mockFollowup.patient.name, patient_reply: content }),
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`${response.status} ${errorText}`);
      }
    const data: ReplyResponse = await response.json();
    setResult(data);
    await refreshEvents();
    setSuggestedReply(data.next_reply ?? "");
      setPatientReply("");
      setIsDetailsOpen(false);
      setStage("review");
    } catch (error) {
      setError(
        error instanceof Error
          ? `分析失败：${error.message}`
          : "分析失败，请稍后重试。"
      );
    } finally {
      setLoading(false);
    }
  }

  async function sendSuggested() {
  const content = suggestedReply.trim();
  if (!content || !result?.assessment.action || loading) return;

  setLoading(true);
  setError(null);

  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/wecom/messages/delivered`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          followup_id: "F001",
          thread_id: threadId,
          actor_id: consultantUserId ?? "consultant_001",
          actor_name: "张三咨询师",
          target_id: "patient_001",
          target_name: mockFollowup.patient.name,
          content,
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`${response.status} ${errorText}`);
    }

    await response.json();
    await refreshEvents();

    if (result.assessment.action === "ASK_MORE") {
      setResult(null);
      setSuggestedReply("");
      setStage("waiting");
    } else {
      setStage(
        result.assessment.action === "NORMAL"
          ? "complete"
          : "escalated"
      );
    }
  } catch (error) {
    setError(
      error instanceof Error
        ? `发送失败：${error.message}`
        : "发送失败，请稍后重试。"
    );
  } finally {
    setLoading(false);
  }
}
  const timelineItems = (events ?? [])
  .filter(
    (event) =>
      (event.event_type === "MESSAGE_DELIVERED" &&
        typeof event.data.content === "string") ||
      (event.event_type === "MESSAGE_GENERATED" &&
        typeof event.data.content === "string") ||
      event.event_type === "ASSESSMENT_COMPLETED"
  )
  .map((event) => {
    if (event.event_type === "ASSESSMENT_COMPLETED") {
      const action = String(event.data.action ?? "");
      const missingFields = Array.isArray(event.data.missing_fields)
        ? event.data.missing_fields.map(String)
        : [];

      return {
        id: `${event.timestamp}-assessment`,
        kind: "assessment" as const,
        author: "AI 判断",
        role: "ai",
        content: missingFields.length
          ? `${action} · 缺失字段：${missingFields.join(", ")}`
          : action,
      };
    }

    if (event.event_type === "MESSAGE_GENERATED") {
      return {
        id: `${event.timestamp}-generated`,
        kind: "generated" as const,
        author: "AI 建议",
        role: "ai",
        content: event.data.content as string,
      };
    }

    return {
      id: `${event.timestamp}-${event.data.actor_role ?? "unknown"}`,
      kind: "message" as const,
      author:
        event.data.actor_role === "patient"
          ? mockFollowup.patient.name
          : event.data.actor_name || "张三咨询师",
      role: event.data.actor_role,
      content: event.data.content as string,
    };
  });

  return <main className="sidebar-shell">
    <header className="topbar"><div className="brand-mark" aria-hidden="true">D</div><div><p className="eyebrow">Dental AI Copilot</p><h1>AI 助手</h1></div></header>

    <section className="section patient-section" aria-labelledby="patient-heading">
      <div className="section-heading-row"><h2 id="patient-heading">患者上下文</h2><span className="case-status">术后回访</span></div>
      <div className="patient-summary"><div className="patient-avatar" aria-hidden="true">杨</div><div className="patient-copy"><strong>{mockFollowup.patient.name}</strong><span>{mockFollowup.patient.treatment} · {mockFollowup.patient.followupDay}</span></div><span className="doctor-name">{mockFollowup.patient.doctor}</span></div>
    </section>

    {stage === "initial" ? <section className="section" aria-labelledby="initial-heading">
      <h2 id="initial-heading">首次回访</h2>
      <textarea className="reply-editor short-editor" aria-label="首次回访消息" value={initialMessage} onChange={(event) => setInitialMessage(event.target.value)} rows={6} />
      <div className="reply-actions"><button className="button button-secondary" type="button" onClick={() => copyText(initialMessage, "initial")}>{copied === "initial" ? "已复制" : "复制"}</button><button className="button button-primary" type="button" disabled={!initialMessage.trim()} onClick={sendInitial}>发送</button></div>
    </section> : <section className="section" aria-labelledby="conversation-heading">
      <h2 id="conversation-heading">对话记录</h2>
      <ol className="conversation-timeline">
  {timelineItems.map((item) =>
    item.kind === "assessment" ? (
      <li className="timeline-status" key={item.id}>
        <span className="message-author">{item.author}</span>
        <p>{item.content}</p>
      </li>
    ) : (
      <li
        className={`timeline-message timeline-${item.role === "patient" ? "patient" : "assistant"}`}
        key={item.id}
      >
        <span className="message-author">{item.author}</span>
        <p>{item.content}</p>
      </li>
    )
  )}

  {stage === "waiting" && (
    <li className="timeline-status status-waiting">等待患者回复</li>
  )}

  {stage === "complete" && (
    <li className="timeline-status status-complete">本次回访已完成</li>
  )}

  {stage === "escalated" && (
    <li className="timeline-status status-escalated">已升级医生处理</li>
  )}
</ol>
    </section>}

    {stage === "waiting" && <section className="section" aria-labelledby="patient-input-heading">
      <h2 id="patient-input-heading">POC 患者回复输入</h2><p className="section-description">仅用于当前 POC，粘贴患者在企微中发送的最新回复</p>
      <textarea className="reply-editor short-editor" aria-label="患者最新回复" value={patientReply} onChange={(event) => setPatientReply(event.target.value)} rows={5} disabled={loading} />
      {error && <p className="error-message" role="alert">{error}</p>}
      <button className="button button-primary analyze-button" type="button" disabled={!patientReply.trim() || loading} onClick={handleAnalyze}>{loading ? "分析中…" : "分析回复"}</button>
    </section>}

    {stage === "review" && result && feedback && <>
      <section className="section" aria-labelledby="assessment-heading">
        <div className="section-heading-row"><h2 id="assessment-heading">AI 判断</h2><span className={`action-badge action-${(result.assessment.action ?? "ASK_MORE").toLowerCase()}`}><span className="status-dot" aria-hidden="true" />{result.assessment.action ?? "ASK_MORE"}</span></div>
        <dl className="feedback-grid">{Object.entries(feedback).map(([key, value]) => { const alert = value === "是" || (key === "pain" && result.patient_feedback.pain_score != null && result.patient_feedback.pain_score >= 7); return <div className="feedback-item" key={key}><dt>{feedbackLabels[key as keyof typeof feedbackLabels]}</dt><dd className={alert ? "value-alert" : value === "未知" ? "value-unknown" : ""}>{value}</dd></div>; })}</dl>
        {!!result.assessment.matched_rules.length && <div className={`matched-rules rules-${(result.assessment.action ?? "ASK_MORE").toLowerCase()}`} aria-label="匹配规则">{result.assessment.matched_rules.map((rule) => <span key={rule}>{rule}</span>)}</div>}
      </section>
      <section className="details-section" aria-labelledby="details-heading">
        <button className="details-trigger" type="button" aria-expanded={isDetailsOpen} aria-controls="assessment-details" onClick={() => setIsDetailsOpen((open) => !open)}><span id="details-heading">AI 判断详情</span><span className={`chevron ${isDetailsOpen ? "chevron-open" : ""}`} aria-hidden="true" /></button>
        {isDetailsOpen && <div className="details-content" id="assessment-details">
          <div className="detail-group"><h3>提取反馈</h3><dl className="detail-list">{Object.entries(feedback).map(([key, value]) => <div key={key}><dt>{feedbackLabels[key as keyof typeof feedbackLabels]}</dt><dd>{value}</dd></div>)}</dl></div>
          <div className="detail-group"><h3>策略动作</h3><p className={`detail-action action-text-${(result.assessment.action ?? "ASK_MORE").toLowerCase()}`}>{result.assessment.action ?? "ASK_MORE"}</p></div>
          <div className="detail-group"><h3>匹配规则</h3><ul className="plain-list">{result.assessment.matched_rules.length ? result.assessment.matched_rules.map((rule) => <li key={rule}>{rule}</li>) : <li>无</li>}</ul></div>
          <div className="detail-group"><h3>缺失字段</h3><ul className="plain-list muted-list">{result.assessment.missing_fields.length ? result.assessment.missing_fields.map((field) => <li key={field}>{field}</li>) : <li>无</li>}</ul></div>
        </div>}
      </section>
      <section className="section" aria-labelledby="suggested-reply-heading">
        <div className="section-heading-row"><h2 id="suggested-reply-heading">建议回复</h2><span className="editable-label">可编辑</span></div>
        <textarea className="reply-editor" aria-label="建议回复" value={suggestedReply} onChange={(event) => setSuggestedReply(event.target.value)} rows={8} />
        <div className="reply-actions"><button className="button button-secondary" type="button" onClick={() => copyText(suggestedReply, "suggested")}>{copied === "suggested" ? "已复制" : "复制"}</button><button className="button button-primary" type="button" disabled={!suggestedReply.trim() || !result.assessment.action} onClick={sendSuggested}>发送</button></div>
      </section>
    </>}
  </main>;
}
