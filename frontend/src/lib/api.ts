import type {
  ChatResponse,
  ConversationExchange,
  DashboardData,
  PropertiesData,
  SchemaData,
  IssuesListResponse,
} from "./types";

const BASE = "/api";

export async function sendChatMessage(
  message: string,
  conversationHistory: ConversationExchange[]
): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_history: conversationHistory }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  return res.json();
}

export async function getDashboard(): Promise<DashboardData> {
  const res = await fetch(`${BASE}/dashboard`);
  if (!res.ok) throw new Error("Dashboard request failed");
  return res.json();
}

export async function getPropertiesOverview(): Promise<PropertiesData> {
  const res = await fetch(`${BASE}/properties/overview`);
  if (!res.ok) throw new Error("Properties request failed");
  return res.json();
}

export async function getSchema(): Promise<SchemaData> {
  const res = await fetch(`${BASE}/schema`);
  if (!res.ok) throw new Error("Schema request failed");
  return res.json();
}

export async function submitIssue(
  question: string,
  whatWentWrong: string,
  severity: string
): Promise<void> {
  const res = await fetch(`${BASE}/issues`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, what_went_wrong: whatWentWrong, severity }),
  });
  if (!res.ok) throw new Error("Issue submission failed");
}

export async function getIssues(password: string): Promise<IssuesListResponse> {
  const res = await fetch(`${BASE}/issues`, {
    headers: { "x-admin-password": password },
  });
  if (!res.ok) {
    if (res.status === 401) throw new Error("Invalid password");
    throw new Error("Failed to fetch issues");
  }
  return res.json();
}

export async function resolveIssue(issueId: number, password: string): Promise<void> {
  const res = await fetch(`${BASE}/issues/${issueId}/resolve`, {
    method: "POST",
    headers: { "x-admin-password": password },
  });
  if (!res.ok) throw new Error("Failed to resolve issue");
}
