export interface ConversationExchange {
  question: string;
  answer: string;
}

export interface ChatResponse {
  intent: "DATA" | "CHAT";
  answer: string;
  sql_query?: string | null;
  data?: Record<string, unknown>[] | null;
  error?: string | null;
}

export interface ChatMessage {
  role: "user" | "ai";
  content: string;
  sql_query?: string | null;
  data?: Record<string, unknown>[] | null;
  error?: string | null;
}

export interface DashboardData {
  kpis: {
    total_units: number;
    avg_occupancy: number;
    total_vacant: number;
    total_residents: number;
  };
  occupancy: { property: string; occupancy: number }[];
  vacancy_bar: { property: string; vacant_rented: number; vacant_unrented: number }[];
  vacancy_pie: { name: string; value: number }[];
  rent: { property: string; avg_rent: number }[];
  revenue: {
    total_rent: number;
    total_other: number;
    total_concessions: number;
    positive: { charge_code: string; amount: number }[];
    negative: { charge_code: string; amount: number }[];
  };
  pipeline: { property: string; applicants: number }[];
  deposits: { property: string; security_deposit: number; other_deposits: number }[];
  lease_expirations: { name: string; unit: string; expiration: string; property: string }[];
  outstanding_balances: { name: string; unit: string; balance: number; property: string }[];
}

export interface PropertiesData {
  metrics: Record<string, number>;
  properties_table: Record<string, unknown>[];
  charge_codes_table: Record<string, unknown>[];
  deposits_table: Record<string, unknown>[];
}

export interface SchemaField {
  name: string;
  type: string;
  note: string;
}

export interface SchemaTable {
  name: string;
  label: string;
  description: string;
  example_query: string;
  fields: SchemaField[];
}

export interface SchemaData {
  stats: { tables: number; total_columns: number; properties: number; engine: string };
  tables: SchemaTable[];
}

export interface IssueResponse {
  id: number;
  timestamp: string;
  question: string;
  what_went_wrong: string;
  severity: string;
  resolved_at?: string | null;
}

export interface IssuesListResponse {
  open_issues: IssueResponse[];
  resolved_issues: IssueResponse[];
  total: number;
  open_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
}
