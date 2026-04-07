"use client";

import { useState, useRef, useEffect } from "react";
import { useChat } from "@/hooks/useChat";
import ChatMessage from "@/components/chat/ChatMessage";
import ChatInput from "@/components/chat/ChatInput";
import ExampleQuestions from "@/components/chat/ExampleQuestions";
import ReportIssueModal from "@/components/chat/ReportIssueModal";

export default function ChatPage() {
  const { messages, isLoading, sendMessage, resetChat, downloadChat } = useChat();
  const [externalValue, setExternalValue] = useState<string | undefined>();
  const [reportQuestion, setReportQuestion] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] max-w-5xl mx-auto">
      {/* Header bar */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)] bg-white/80 backdrop-blur-sm">
        <div>
          <h1 className="text-xl font-extrabold text-[var(--foreground)]">
            <span style={{ color: "var(--cyan-deep)" }}>AI</span> Chat
          </h1>
          <p className="text-xs text-[var(--muted)] mt-0.5">
            Ask questions about your properties in plain English
          </p>
        </div>
        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <>
              <button
                onClick={downloadChat}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-[var(--border)] text-[var(--muted)] hover:text-[var(--foreground)] hover:border-[var(--cyan)] transition-all"
              >
                Export
              </button>
              <button
                onClick={resetChat}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-[var(--border)] text-[var(--muted)] hover:text-[var(--rose)] hover:border-[var(--rose)] transition-all"
              >
                Clear
              </button>
            </>
          )}
        </div>
      </div>

      {/* Messages area */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full gap-8">
            <div className="text-center space-y-2">
              <div
                className="text-5xl font-black bg-clip-text text-transparent"
                style={{ backgroundImage: "var(--gradient-hero)" }}
              >
                Ask Anything
              </div>
              <p className="text-sm text-[var(--muted)] max-w-md">
                Query your property data using natural language. I&apos;ll translate your
                questions into SQL and return insights instantly.
              </p>
            </div>
            <ExampleQuestions onSelect={(q) => setExternalValue(q)} />
          </div>
        ) : (
          messages.map((msg, i) => (
            <ChatMessage
              key={i}
              message={msg}
              onReportIssue={(q) => setReportQuestion(q)}
            />
          ))
        )}

        {isLoading && (
          <div className="flex items-start gap-3 mb-5">
            <div className="w-9 h-9 rounded-full bg-[var(--surface)] border border-[var(--border)] flex items-center justify-center flex-shrink-0">
              <span className="w-4 h-4 border-2 border-[var(--cyan)] border-t-transparent rounded-full animate-spin" />
            </div>
            <div className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl rounded-bl-sm px-5 py-3">
              <span className="text-sm text-[var(--muted)]">Analyzing your question...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput
        onSend={sendMessage}
        isLoading={isLoading}
        externalValue={externalValue}
        onExternalValueConsumed={() => setExternalValue(undefined)}
      />

      {/* Report modal */}
      {reportQuestion && (
        <ReportIssueModal
          question={reportQuestion}
          onClose={() => setReportQuestion(null)}
        />
      )}
    </div>
  );
}
