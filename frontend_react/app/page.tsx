"use client";

import { useEffect, useRef, useState } from "react";
import { mockFollowup } from "../data/mockFollowup";

const feedbackLabels = {
  pain: "疼痛",
  currentBleeding: "当前出血",
  swelling: "肿胀",
  fever: "发烧",
} as const;

type ReplyResponse = {
  action: "NORMAL" | "ASK_MORE" | "ESCALATE" | null;
  matched_rules: string[];
  missing_fields: string[];
  next_reply: string | null;
  doctor_notification: string | null;
  pain_score: number | null;
  current_bleeding: boolean | null;
  swelling: boolean | null;
  fever: boolean | null;
};

function yesNoUnknown(value: boolean | null) {
  if (value === null) return "Unknown";
  return value ? "Yes" : "No";
}

export default function Home() {
  const [reply, setReply] = useState(mockFollowup.suggestedReply);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [result, setResult] = useState<ReplyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const hasLoaded = useRef(false);

  useEffect(() => {
    if (hasLoaded.current) return;
    hasLoaded.current = true;

    async function loadAssessment() {
      try {
        const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_BASE_URL}/followups/reply`,
  {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      followup_id: "F001",
      patient_id: "P001",
      treatment_id: "T001",
      patient_name: mockFollowup.patient.name,
      patient_reply: mockFollowup.latestPatientMessage,
    }),
  }
);

        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`);
        }

        const data: ReplyResponse = await response.json();

        setResult(data);
        setReply(data.next_reply ?? "");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    }

    loadAssessment();
  }, []);

  const extractedFeedback = {
    pain:
      result?.pain_score == null
        ? "Unknown"
        : `${result.pain_score}/10`,
    currentBleeding: yesNoUnknown(result?.current_bleeding ?? null),
    swelling: yesNoUnknown(result?.swelling ?? null),
    fever: yesNoUnknown(result?.fever ?? null),
  };

  const action = result?.action ?? mockFollowup.action;
  const matchedRules = result?.matched_rules ?? [];
  const missingFields = result?.missing_fields ?? [];

  async function copyReply() {
    await navigator.clipboard.writeText(reply);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <main className="sidebar-shell">
      <header className="topbar">
        <div className="brand-mark" aria-hidden="true">D</div>
        <div>
          <p className="eyebrow">Dental AI Copilot</p>
          <h1>AI 助手</h1>
        </div>
      </header>

      <section className="section patient-section" aria-labelledby="patient-heading">
        <div className="section-heading-row">
          <h2 id="patient-heading">患者 上下文</h2>
          <span className="case-status">术后回访</span>
        </div>
        <div className="patient-summary">
          <div className="patient-avatar" aria-hidden="true">杨</div>
          <div className="patient-copy">
            <strong>{mockFollowup.patient.name}</strong>
            <span>{mockFollowup.patient.treatment} · {mockFollowup.patient.followupDay}</span>
          </div>
          <span className="doctor-name">{mockFollowup.patient.doctor}</span>
        </div>
      </section>

      <section className="section" aria-labelledby="latest-reply-heading">
        <h2 id="latest-reply-heading">Latest Patient Reply</h2>
        <blockquote className="patient-message">
          <span className="message-author">杨女士 · 刚刚</span>
          <p>{mockFollowup.latestPatientMessage}</p>
        </blockquote>
      </section>

      {loading && <p>AI assessment loading...</p>}
      {error && <p>{error}</p>}

      <section className="section" aria-labelledby="assessment-heading">
        <div className="section-heading-row">
          <h2 id="assessment-heading">AI Assessment</h2>
          <span className={`action-badge action-${action.toLowerCase()}`}>
            <span className="status-dot" aria-hidden="true" />
            {action}
          </span>
        </div>
        <dl className="feedback-grid">
          {Object.entries(extractedFeedback).map(([key, value]) => (
            <div className="feedback-item" key={key}>
              <dt>{feedbackLabels[key as keyof typeof feedbackLabels]}</dt>
              <dd className={value === "Yes" || value === "8/10" ? "value-alert" : value === "Unknown" ? "value-unknown" : ""}>
                {value}
              </dd>
            </div>
          ))}
        </dl>
        <div className="matched-rules" aria-label="Matched rules">
          {matchedRules.map((rule) => <span key={rule}>{rule}</span>)}
        </div>
      </section>

      <section className="section" aria-labelledby="suggested-reply-heading">
        <div className="section-heading-row">
          <h2 id="suggested-reply-heading">Suggested Reply</h2>
          <span className="editable-label">可编辑</span>
        </div>
        <textarea
          className="reply-editor"
          aria-label="Suggested reply"
          value={reply}
          onChange={(event) => setReply(event.target.value)}
          rows={8}
        />
        <div className="reply-actions">
          <button className="button button-secondary" type="button" onClick={copyReply}>
            {copied ? "Copied" : "Copy"}
          </button>
          <button
            className="button button-primary"
            type="button"
            disabled
            title="WeCom integration pending"
          >
            Send
          </button>
        </div>
      </section>

      <section className="details-section" aria-labelledby="details-heading">
        <button
          className="details-trigger"
          type="button"
          aria-expanded={isDetailsOpen}
          aria-controls="assessment-details"
          onClick={() => setIsDetailsOpen((open) => !open)}
        >
          <span id="details-heading">AI 判断详情</span>
          <span className={`chevron ${isDetailsOpen ? "chevron-open" : ""}`} aria-hidden="true" />
        </button>
        {isDetailsOpen && (
          <div className="details-content" id="assessment-details">
            <div className="detail-group">
              <h3>Extracted Feedback</h3>
              <dl className="detail-list">
                {Object.entries(extractedFeedback).map(([key, value]) => (
                  <div key={key}>
                    <dt>{feedbackLabels[key as keyof typeof feedbackLabels]}</dt>
                    <dd>{value}</dd>
                  </div>
                ))}
              </dl>
            </div>
            <div className="detail-group">
              <h3>Policy Action</h3>
              <p className="detail-action">{action}</p>
            </div>
            <div className="detail-group">
              <h3>Matched Rules</h3>
              <ul className="plain-list">
                {matchedRules.map((rule) => <li key={rule}>{rule}</li>)}
              </ul>
            </div>
            <div className="detail-group">
              <h3>Missing Fields</h3>
              <ul className="plain-list muted-list">
                {missingFields.map((field) => <li key={field}>{field}</li>)}
              </ul>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
