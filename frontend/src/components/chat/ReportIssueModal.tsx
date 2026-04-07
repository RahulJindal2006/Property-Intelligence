"use client";

import { useState } from "react";
import { submitIssue } from "@/lib/api";

interface Props {
  question: string;
  onClose: () => void;
}

export default function ReportIssueModal({ question, onClose }: Props) {
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("Low");
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

  const handleSubmit = async () => {
    if (!description.trim()) return;
    setStatus("submitting");
    try {
      await submitIssue(question, description, severity);
      setStatus("success");
      setTimeout(onClose, 1500);
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div
        className="bg-white border border-[var(--border)] rounded-2xl p-6 w-full max-w-md space-y-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold">Report an Issue</h3>
          <button onClick={onClose} className="text-[var(--muted)] hover:text-[var(--foreground)] text-lg">
            ✕
          </button>
        </div>

        <div>
          <label className="block text-xs font-semibold text-[var(--muted)] mb-1.5 uppercase tracking-wider">
            What went wrong?
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-3 text-sm text-[var(--foreground)] placeholder:text-[var(--dimmed)] focus:outline-none focus:border-[var(--cyan)] focus:ring-2 focus:ring-[var(--cyan)]/20 resize-none h-24"
            placeholder="Describe the issue..."
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-[var(--muted)] mb-1.5 uppercase tracking-wider">
            Severity
          </label>
          <select
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="w-full bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-2.5 text-sm text-[var(--foreground)] focus:outline-none focus:border-[var(--cyan)]"
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>

        {status === "success" && (
          <div className="text-sm font-medium" style={{ color: "var(--emerald)" }}>Issue reported successfully!</div>
        )}
        {status === "error" && (
          <div className="text-sm font-medium" style={{ color: "var(--rose)" }}>Failed to submit. Please try again.</div>
        )}

        <button
          onClick={handleSubmit}
          disabled={!description.trim() || status === "submitting" || status === "success"}
          className="w-full text-white rounded-xl px-4 py-2.5 text-sm font-bold transition-all hover:shadow-lg disabled:opacity-40 shadow-md"
          style={{ background: "var(--gradient-cyan)" }}
        >
          {status === "submitting" ? "Submitting..." : "Submit Report"}
        </button>
      </div>
    </div>
  );
}
