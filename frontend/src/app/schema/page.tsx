"use client";

import { useEffect, useState } from "react";
import { getSchema } from "@/lib/api";
import type { SchemaData } from "@/lib/types";
import PageHeader from "@/components/layout/PageHeader";

const TAB_COLORS = ["var(--cyan-deep)", "var(--magenta)", "var(--lime)", "var(--orange)"];

export default function SchemaPage() {
  const [data, setData] = useState<SchemaData | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSchema()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-[var(--muted)]">Loading...</div>;
  if (!data) return <div className="p-8" style={{ color: "var(--rose)" }}>Failed to load schema.</div>;

  const table = data.tables[activeTab];
  const activeColor = TAB_COLORS[activeTab % TAB_COLORS.length];

  return (
    <div className="p-8 w-full">
      <PageHeader
        label="DATABASE"
        title="Database Schema"
        subtitle="Four SQLite tables power the Property Management AI Assistant. Every question you ask is translated into a query against one or more of these tables."
        color="var(--lime)"
      />

      {/* Stats bar */}
      <div className="flex gap-4 mb-9 flex-wrap">
        {[
          { value: data.stats.tables, label: "TABLES", color: "var(--cyan-deep)" },
          { value: data.stats.total_columns, label: "TOTAL COLUMNS", color: "var(--magenta)" },
          { value: data.stats.properties, label: "PROPERTIES", color: "var(--lime)" },
          { value: data.stats.engine, label: "DATABASE ENGINE", color: "var(--orange)" },
        ].map((s) => (
          <div key={s.label} className="flex-1 min-w-[120px] bg-white border border-[var(--border)] rounded-xl px-6 py-4 text-center shadow-sm">
            <div className="text-2xl font-extrabold mb-1" style={{ color: s.color }}>{s.value}</div>
            <div className="text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Tab buttons */}
      <div className="flex gap-2 border-b border-[var(--border)] mb-6 flex-wrap">
        {data.tables.map((t, i) => (
          <button
            key={t.name}
            onClick={() => setActiveTab(i)}
            className={`px-5 py-2.5 text-xs font-bold tracking-wider uppercase rounded-t-lg transition-all
              ${activeTab === i
                ? "text-white shadow-md"
                : "text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--surface)]"
              }`}
            style={activeTab === i ? { background: TAB_COLORS[i % TAB_COLORS.length] } : undefined}
          >
            {t.name}
          </button>
        ))}
      </div>

      {/* Active table */}
      <div>
        <div
          className="text-[11px] font-bold tracking-[0.12em] uppercase mb-2"
          style={{ color: activeColor }}
        >
          {table.label}
        </div>
        <h2 className="text-xl font-extrabold tracking-tight text-[var(--foreground)] mb-2 uppercase">{table.name}</h2>
        <p className="text-sm text-[var(--muted)] leading-relaxed mb-6">{table.description}</p>

        <div className="space-y-2.5 mb-8">
          {table.fields.map((field) => (
            <div
              key={field.name}
              className="bg-white border border-[var(--border)] rounded-xl px-4 py-3 flex items-center justify-between gap-4 hover:shadow-sm transition-shadow"
            >
              <div>
                <div className="text-[13px] font-bold font-mono text-[var(--foreground)]">{field.name}</div>
                <div className="text-[11px] text-[var(--muted)] mt-0.5">{field.note}</div>
              </div>
              <span
                className="text-[11px] font-bold rounded px-2 py-0.5 whitespace-nowrap"
                style={{
                  color: activeColor,
                  background: `color-mix(in srgb, ${activeColor} 10%, transparent)`,
                }}
              >
                {field.type}
              </span>
            </div>
          ))}
        </div>

        <div className="bg-slate-900 border border-slate-700 rounded-xl overflow-hidden shadow-sm">
          <div className="px-4 py-2 border-b border-slate-700">
            <span className="text-[10px] font-bold tracking-widest text-slate-400 uppercase">Example Query</span>
          </div>
          <pre className="px-4 py-3 text-[13px] text-cyan-300 font-mono whitespace-pre-wrap overflow-x-auto">
            {table.example_query}
          </pre>
        </div>
      </div>
    </div>
  );
}
