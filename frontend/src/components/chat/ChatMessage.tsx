"use client";

import Image from "next/image";
import { useState } from "react";
import type { ChatMessage as ChatMessageType } from "@/lib/types";
import SqlViewer from "./SqlViewer";
import DataTable from "./DataTable";

interface Props {
  message: ChatMessageType;
  onReportIssue?: (question: string) => void;
}

export default function ChatMessage({ message, onReportIssue }: Props) {
  const [showSql, setShowSql] = useState(false);

  if (message.role === "user") {
    return (
      <div className="flex justify-end mb-5">
        <div
          className="text-white rounded-2xl rounded-br-sm px-5 py-3 max-w-[70%] text-[15px] leading-relaxed shadow-md"
          style={{ background: "var(--gradient-cyan)" }}
        >
          {message.content}
        </div>
      </div>
    );
  }

  const isError = message.error === "blocked" || message.error === "network_error";

  return (
    <div className="flex items-start gap-3 mb-5">
      <Image
        src="/logo.svg"
        alt="AI Assistant"
        width={36}
        height={36}
        className="rounded-full flex-shrink-0 mt-0.5 ring-2 ring-[var(--border)]"
      />
      <div className="max-w-[75%] space-y-3">
        <div
          className={`rounded-2xl rounded-bl-sm px-5 py-3 text-[15px] leading-relaxed ${
            isError
              ? "bg-red-50 border border-red-200 text-[var(--rose)]"
              : "bg-[var(--surface)] border border-[var(--border)]"
          }`}
        >
          {message.content}
        </div>

        {message.data && message.data.length > 0 && (
          <DataTable data={message.data} />
        )}

        <div className="flex items-center gap-2 flex-wrap">
          {message.sql_query && (
            <button
              onClick={() => setShowSql(!showSql)}
              className="text-xs font-semibold px-3 py-1 rounded-full border transition-all"
              style={{
                color: "var(--cyan-deep)",
                borderColor: "rgba(0,229,255,0.3)",
                background: "rgba(0,229,255,0.06)",
              }}
            >
              {showSql ? "Hide SQL" : "Show SQL"}
            </button>
          )}
          {onReportIssue && !isError && (
            <button
              onClick={() => onReportIssue(message.content)}
              className="text-xs text-[var(--dimmed)] hover:text-[var(--rose)] transition-colors"
            >
              Report Issue
            </button>
          )}
        </div>

        {showSql && message.sql_query && <SqlViewer sql={message.sql_query} />}
      </div>
    </div>
  );
}
