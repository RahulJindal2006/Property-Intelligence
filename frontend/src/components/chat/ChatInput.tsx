"use client";

import { useState, useRef, useEffect } from "react";

interface Props {
  onSend: (message: string) => void;
  isLoading: boolean;
  externalValue?: string;
  onExternalValueConsumed?: () => void;
}

export default function ChatInput({
  onSend,
  isLoading,
  externalValue,
  onExternalValueConsumed,
}: Props) {
  const [input, setInput] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (externalValue) {
      onSend(externalValue);
      onExternalValueConsumed?.();
    }
  }, [externalValue, onSend, onExternalValueConsumed]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSend(input.trim());
    setInput("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-3 p-4 border-t border-[var(--border)] bg-white/90 backdrop-blur-sm"
    >
      <input
        ref={inputRef}
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask anything about your properties..."
        className="flex-1 bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-3 text-sm text-[var(--foreground)] placeholder:text-[var(--dimmed)] focus:outline-none focus:border-[var(--cyan)] focus:ring-2 focus:ring-[var(--cyan)]/20 transition-all"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="text-white rounded-xl px-6 py-3 text-sm font-bold transition-all hover:scale-105 hover:shadow-lg disabled:opacity-40 disabled:hover:scale-100 shadow-md"
        style={{ background: "var(--gradient-cyan)" }}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Thinking
          </span>
        ) : (
          "Send"
        )}
      </button>
    </form>
  );
}
