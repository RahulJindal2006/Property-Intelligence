"use client";

import { useState, useMemo } from "react";
import Image from "next/image";
import { getIssues, resolveIssue } from "@/lib/api";
import type { IssuesListResponse, IssueResponse } from "@/lib/types";
import PageHeader from "@/components/layout/PageHeader";

const SEVERITY_STYLES: Record<string, { bg: string; text: string; border: string; glow: string }> = {
  High: { bg: "rgba(244,63,94,0.08)", text: "var(--rose)", border: "var(--rose)", glow: "rgba(244,63,94,0.15)" },
  Medium: { bg: "rgba(249,115,22,0.08)", text: "var(--orange)", border: "var(--orange)", glow: "rgba(249,115,22,0.15)" },
  Low: { bg: "rgba(0,151,167,0.08)", text: "var(--cyan-deep)", border: "var(--cyan-deep)", glow: "rgba(0,151,167,0.15)" },
};

function timeAgo(timestamp: string): string {
  const now = Date.now();
  const then = new Date(timestamp).getTime();
  const diff = now - then;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "Just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  return new Date(timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function severityBadge(severity: string) {
  const style = SEVERITY_STYLES[severity] || SEVERITY_STYLES.Low;
  return (
    <span
      className="text-[11px] font-bold tracking-wider rounded-full px-2.5 py-0.5 uppercase"
      style={{ background: style.bg, color: style.text }}
    >
      {severity}
    </span>
  );
}

function IssueCard({ issue, onResolve, isResolving }: { issue: IssueResponse; onResolve?: (id: number) => void; isResolving?: boolean }) {
  const [confirmOpen, setConfirmOpen] = useState(false);
  const style = SEVERITY_STYLES[issue.severity] || SEVERITY_STYLES.Low;

  return (
    <div
      className="bg-white border border-[var(--border)] border-l-4 rounded-xl px-5 py-4 mb-3 shadow-sm hover:shadow-md transition-all"
      style={{ borderLeftColor: style.border }}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3 flex-wrap">
          {severityBadge(issue.severity)}
          <span className="text-xs text-[var(--muted)]" title={new Date(issue.timestamp).toLocaleString()}>
            {timeAgo(issue.timestamp)}
          </span>
          <span className="text-[10px] text-[var(--dimmed)] font-mono">#{issue.id}</span>
        </div>
      </div>
      <div className="text-[15px] font-bold text-[var(--foreground)] mb-1">{issue.question}</div>
      <div className="text-[13px] text-[var(--muted)] leading-relaxed">{issue.what_went_wrong}</div>
      {onResolve && (
        <div className="mt-3">
          {!confirmOpen ? (
            <button
              onClick={() => setConfirmOpen(true)}
              className="text-xs font-semibold rounded-full px-4 py-1.5 transition-all hover:shadow-sm"
              style={{
                color: "var(--emerald)",
                background: "rgba(16,185,129,0.08)",
                border: "1px solid rgba(16,185,129,0.25)",
              }}
            >
              Resolve
            </button>
          ) : (
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--muted)]">Confirm?</span>
              <button
                onClick={() => { onResolve(issue.id); setConfirmOpen(false); }}
                disabled={isResolving}
                className="text-xs font-bold text-white rounded-full px-4 py-1.5 transition-all hover:shadow-sm disabled:opacity-40"
                style={{ background: "var(--emerald)" }}
              >
                {isResolving ? "..." : "Yes, Resolve"}
              </button>
              <button
                onClick={() => setConfirmOpen(false)}
                className="text-xs font-semibold text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

type SortKey = "newest" | "oldest" | "severity";

export default function IssuesPage() {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [data, setData] = useState<IssuesListResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortKey>("newest");
  const [resolvingId, setResolvingId] = useState<number | null>(null);
  const [tab, setTab] = useState<"open" | "resolved">("open");

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    try {
      const result = await getIssues(password);
      setData(result);
      setAuthenticated(true);
    } catch {
      setError("Incorrect password. Access denied.");
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (issueId: number) => {
    setResolvingId(issueId);
    try {
      await resolveIssue(issueId, password);
      const result = await getIssues(password);
      setData(result);
    } catch {
      alert("Failed to resolve issue.");
    } finally {
      setResolvingId(null);
    }
  };

  const handleLogout = () => {
    setAuthenticated(false);
    setData(null);
    setPassword("");
    setSearch("");
    setFilter("All");
    setSort("newest");
  };

  const severityOrder: Record<string, number> = { High: 0, Medium: 1, Low: 2 };

  const filteredOpen = useMemo(() => {
    let issues = data?.open_issues ?? [];
    if (filter !== "All") issues = issues.filter((i) => i.severity === filter);
    if (search.trim()) {
      const q = search.toLowerCase();
      issues = issues.filter((i) =>
        i.question.toLowerCase().includes(q) || i.what_went_wrong.toLowerCase().includes(q)
      );
    }
    if (sort === "oldest") issues = [...issues].reverse();
    if (sort === "severity") issues = [...issues].sort((a, b) => (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3));
    return issues;
  }, [data, filter, search, sort]);

  // ── LOGIN SCREEN ──
  if (!authenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen p-8">
        <div className="w-full max-w-md">
          {/* Card */}
          <div className="relative bg-white border border-[var(--border)] rounded-3xl px-10 py-14 shadow-xl overflow-hidden">
            {/* Gradient accent bar */}
            <div className="absolute top-0 left-0 right-0 h-1.5" style={{ background: "var(--gradient-hero)" }} />

            {/* Decorative blurs */}
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full opacity-15 blur-3xl" style={{ background: "var(--cyan)" }} />
            <div className="absolute -bottom-20 -left-20 w-40 h-40 rounded-full opacity-10 blur-3xl" style={{ background: "var(--magenta)" }} />

            <div className="relative z-10">
              {/* Logo */}
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg" style={{ background: "var(--gradient-hero)" }}>
                  <Image src="/logo.svg" alt="Logo" width={40} height={40} />
                </div>
              </div>

              <h2 className="text-2xl font-extrabold text-[var(--foreground)] text-center mb-1">Admin Console</h2>
              <p className="text-[13px] text-[var(--muted)] text-center leading-relaxed mb-8">
                Enter your credentials to access issue reports and management tools.
              </p>

              {/* Input */}
              <div className="mb-4">
                <label className="text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase mb-2 block">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); setError(""); }}
                    onKeyDown={(e) => e.key === "Enter" && handleLogin()}
                    placeholder="Enter admin password"
                    className="w-full bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-3.5 pr-12 text-sm text-[var(--foreground)] placeholder:text-[var(--muted)] focus:outline-none focus:border-[var(--cyan)] focus:ring-2 focus:ring-[var(--cyan)]/20 transition-all"
                    autoFocus
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--muted)] hover:text-[var(--foreground)] transition-colors text-sm"
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="flex items-center gap-2 mb-4 px-3 py-2.5 rounded-xl" style={{ background: "rgba(244,63,94,0.06)", border: "1px solid rgba(244,63,94,0.15)" }}>
                  <span className="text-sm" style={{ color: "var(--rose)" }}>&#10007;</span>
                  <span className="text-xs font-medium" style={{ color: "var(--rose)" }}>{error}</span>
                </div>
              )}

              {/* Button */}
              <button
                onClick={handleLogin}
                disabled={loading || !password.trim()}
                className="w-full text-white rounded-xl px-4 py-3.5 text-sm font-bold transition-all hover:shadow-lg hover:scale-[1.02] disabled:opacity-40 disabled:hover:scale-100 shadow-md"
                style={{ background: "var(--gradient-hero)" }}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Authenticating...
                  </span>
                ) : "Sign In"}
              </button>

              {/* Security note */}
              <p className="text-[10px] text-[var(--dimmed)] text-center mt-5">
                Protected endpoint. All access attempts are logged.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const resolvedRate = data.total > 0 ? Math.round((data.resolved_issues.length / data.total) * 100) : 0;

  // ── DASHBOARD ──
  return (
    <div className="p-8 w-full">
      {/* Header row */}
      <div className="flex items-start justify-between mb-2 flex-wrap gap-4">
        <PageHeader label="ADMIN CONSOLE" title="Issue Reports" subtitle="Monitor, triage, and resolve issues reported by users." color="var(--rose)" />
        <div className="flex items-center gap-2 mt-2">
          <button
            onClick={() => {
              const csv = [
                "ID,Timestamp,Question,What_Went_Wrong,Severity,Status",
                ...data.open_issues.map((i) => `${i.id},"${i.timestamp}","${i.question}","${i.what_went_wrong}","${i.severity}","Open"`),
                ...data.resolved_issues.map((i) => `${i.id},"${i.timestamp}","${i.question}","${i.what_went_wrong}","${i.severity}","Resolved"`),
              ].join("\n");
              const blob = new Blob([csv], { type: "text/csv" });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = `issues_${new Date().toISOString().slice(0, 10)}.csv`;
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="text-xs font-semibold px-4 py-1.5 rounded-full border border-[var(--border)] text-[var(--muted)] hover:text-[var(--foreground)] hover:border-[var(--cyan)] transition-all"
          >
            Export CSV
          </button>
          <button
            onClick={handleLogout}
            className="text-xs font-semibold text-[var(--muted)] hover:text-[var(--rose)] border border-[var(--border)] rounded-full px-4 py-1.5 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
        {[
          { label: "Total", value: data.total, color: "var(--foreground)" },
          { label: "Open", value: data.open_count, color: "var(--cyan-deep)" },
          { label: "Resolved", value: data.resolved_issues.length, color: "var(--emerald)" },
          { label: "High", value: data.high_count, color: "var(--rose)" },
          { label: "Medium", value: data.medium_count, color: "var(--orange)" },
          { label: "Resolution Rate", value: `${resolvedRate}%`, color: "var(--lime)" },
        ].map((m) => (
          <div key={m.label} className="bg-white border border-[var(--border)] rounded-xl px-4 py-3 text-center shadow-sm">
            <div className="text-xl font-extrabold" style={{ color: m.color }}>{m.value}</div>
            <div className="text-[10px] font-bold tracking-wider text-[var(--muted)] uppercase">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 mb-6 border-b border-[var(--border)]">
        <button
          onClick={() => setTab("open")}
          className={`px-5 py-2.5 text-xs font-bold tracking-wider uppercase rounded-t-lg transition-all ${
            tab === "open"
              ? "text-white shadow-sm"
              : "text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--surface)]"
          }`}
          style={tab === "open" ? { background: "var(--rose)" } : undefined}
        >
          Open ({data.open_count})
        </button>
        <button
          onClick={() => setTab("resolved")}
          className={`px-5 py-2.5 text-xs font-bold tracking-wider uppercase rounded-t-lg transition-all ${
            tab === "resolved"
              ? "text-white shadow-sm"
              : "text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--surface)]"
          }`}
          style={tab === "resolved" ? { background: "var(--emerald)" } : undefined}
        >
          Resolved ({data.resolved_issues.length})
        </button>
      </div>

      {/* Controls bar */}
      {tab === "open" && (
        <div className="flex items-center gap-3 mb-6 flex-wrap">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)] text-sm">&#128269;</span>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search issues..."
              className="w-full bg-[var(--surface)] border border-[var(--border)] rounded-xl pl-9 pr-4 py-2 text-sm text-[var(--foreground)] placeholder:text-[var(--muted)] focus:outline-none focus:border-[var(--cyan)] transition-all"
            />
          </div>
          {/* Filter */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-2 text-sm text-[var(--foreground)] focus:outline-none focus:border-[var(--cyan)]"
          >
            <option value="All">All Severities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          {/* Sort */}
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as SortKey)}
            className="bg-[var(--surface)] border border-[var(--border)] rounded-xl px-4 py-2 text-sm text-[var(--foreground)] focus:outline-none focus:border-[var(--cyan)]"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="severity">By Severity</option>
          </select>
        </div>
      )}

      {/* ── OPEN TAB ── */}
      {tab === "open" && (
        <>
          {filteredOpen.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-4xl mb-3">&#10003;</div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-1">
                {search || filter !== "All" ? "No matching issues" : "All clear!"}
              </h3>
              <p className="text-sm text-[var(--muted)]">
                {search || filter !== "All" ? "Try adjusting your search or filter." : "No open issues at the moment."}
              </p>
            </div>
          ) : (
            <div>
              {filteredOpen.map((issue) => (
                <IssueCard
                  key={issue.id}
                  issue={issue}
                  onResolve={handleResolve}
                  isResolving={resolvingId === issue.id}
                />
              ))}
            </div>
          )}
        </>
      )}

      {/* ── RESOLVED TAB ── */}
      {tab === "resolved" && (
        <>
          {data.resolved_issues.length === 0 ? (
            <div className="text-center py-16">
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-1">No resolved issues yet</h3>
              <p className="text-sm text-[var(--muted)]">Resolved issues will appear here.</p>
            </div>
          ) : (
            <div>
              {data.resolved_issues.map((issue) => (
                <div
                  key={issue.id}
                  className="bg-white border border-[var(--border)] border-l-4 rounded-xl px-5 py-4 mb-3 opacity-80 hover:opacity-100 transition-opacity"
                  style={{ borderLeftColor: "var(--emerald)" }}
                >
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <span
                      className="text-[11px] font-bold tracking-wider rounded-full px-2.5 py-0.5 uppercase"
                      style={{ background: "rgba(16,185,129,0.08)", color: "var(--emerald)" }}
                    >
                      RESOLVED
                    </span>
                    {severityBadge(issue.severity)}
                    <span className="text-xs text-[var(--muted)]">
                      Reported {timeAgo(issue.timestamp)}
                    </span>
                    {issue.resolved_at && (
                      <span className="text-xs text-[var(--muted)]">
                        · Closed {issue.resolved_at}
                      </span>
                    )}
                    <span className="text-[10px] text-[var(--dimmed)] font-mono">#{issue.id}</span>
                  </div>
                  <div className="text-[15px] font-bold text-[var(--foreground)] mb-1">{issue.question}</div>
                  <div className="text-[13px] text-[var(--muted)]">{issue.what_went_wrong}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
