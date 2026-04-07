"use client";

import { useState, useCallback } from "react";
import type { ChatMessage, ConversationExchange } from "@/lib/types";
import { sendChatMessage } from "@/lib/api";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState<ConversationExchange[]>([]);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!message.trim() || isLoading) return;

      // Add user message immediately
      setMessages((prev) => [...prev, { role: "user", content: message }]);
      setIsLoading(true);

      try {
        const response = await sendChatMessage(message, conversationHistory.slice(-3));

        // Add AI message
        setMessages((prev) => [
          ...prev,
          {
            role: "ai",
            content: response.answer,
            sql_query: response.sql_query,
            data: response.data,
            error: response.error,
          },
        ]);

        // Update conversation history
        setConversationHistory((prev) => [
          ...prev,
          { question: message, answer: response.answer },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "ai",
            content: "Sorry, something went wrong. Please try again.",
            error: "network_error",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, conversationHistory]
  );

  const resetChat = useCallback(() => {
    setMessages([]);
    setConversationHistory([]);
  }, []);

  const downloadChat = useCallback(() => {
    let text = "";
    for (const msg of messages) {
      if (msg.role === "user") {
        text += `You: ${msg.content}\n`;
      } else {
        text += `AI: ${msg.content}\n`;
        if (msg.sql_query) text += `SQL: ${msg.sql_query}\n`;
      }
      text += "\n";
    }
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `conversation_${new Date().toISOString().slice(0, 19).replace(/[:-]/g, "")}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }, [messages]);

  return { messages, isLoading, sendMessage, resetChat, downloadChat };
}
