"use client";

import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, LineChart, Line, AreaChart, Area,
  RadialBarChart, RadialBar,
} from "recharts";
import { getDashboard } from "@/lib/api";
import type { DashboardData } from "@/lib/types";
import PageHeader from "@/components/layout/PageHeader";
import KpiCard from "@/components/dashboard/KpiCard";
import SectionHeader from "@/components/dashboard/SectionHeader";

const CYAN = "#00e5ff";
const CYAN_DEEP = "#0097a7";
const MAGENTA = "#d946ef";
const LIME = "#84cc16";
const ORANGE = "#f97316";
const ROSE = "#f43f5e";
const BLUE = "#3b82f6";
const EMERALD = "#10b981";
const FOREGROUND = "#1a1a2e";
const MUTED = "#6b7280";

function occColor(val: number) {
  if (val < 90) return ROSE;
  if (val < 95) return ORANGE;
  return CYAN_DEEP;
}

const tooltipStyle = {
  contentStyle: {
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "12px",
    fontSize: "13px",
    color: FOREGROUND,
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
  },
  labelStyle: { color: FOREGROUND, fontWeight: 700 },
};

const CHART_CARD = "bg-white border border-[var(--border)] rounded-2xl p-5 shadow-sm";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8">
        <PageHeader label="INTELLIGENCE" title="Property Insights Dashboard" subtitle="Loading..." />
        <div className="grid grid-cols-4 gap-4 animate-pulse">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-24 bg-[var(--surface)] rounded-2xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!data) return <div className="p-8 text-[var(--rose)]">Failed to load dashboard data.</div>;

  const { kpis, occupancy, vacancy_bar, vacancy_pie, rent, revenue, pipeline, deposits, lease_expirations, outstanding_balances } = data;

  // Derived data for additional charts
  const occupancyRadial = occupancy.slice(0, 8).map((p, i) => ({
    name: p.property.length > 15 ? p.property.slice(0, 15) + "…" : p.property,
    occupancy: p.occupancy,
    fill: [CYAN, MAGENTA, LIME, ORANGE, BLUE, EMERALD, ROSE, CYAN_DEEP][i % 8],
  }));

  const rentVsDeposit = rent.map((r) => {
    const dep = deposits.find((d) => d.property === r.property);
    return {
      property: r.property.length > 12 ? r.property.slice(0, 12) + "…" : r.property,
      avg_rent: r.avg_rent,
      security_deposit: dep?.security_deposit ?? 0,
    };
  });

  const pipelineWithColor = pipeline.map((p, i) => ({
    ...p,
    property: p.property.length > 15 ? p.property.slice(0, 15) + "…" : p.property,
    fill: [CYAN, MAGENTA, LIME, ORANGE, BLUE, EMERALD, ROSE, CYAN_DEEP][i % 8],
  }));

  return (
    <div className="p-8 w-full">
      <PageHeader
        label="INTELLIGENCE"
        title="Property Insights Dashboard"
        subtitle="Live portfolio metrics pulled directly from the property management database."
        color={CYAN_DEEP}
      />

      {/* KPI Cards */}
      <div className="flex gap-4 mb-8 flex-wrap">
        <KpiCard label="Total Units" value={kpis.total_units} subtitle="Across all properties" color={CYAN_DEEP} />
        <KpiCard label="Avg Occupancy" value={`${kpis.avg_occupancy}%`} subtitle="Portfolio average" color={MAGENTA} />
        <KpiCard label="Total Vacant" value={kpis.total_vacant} subtitle="Units available to lease" color={ROSE} />
        <KpiCard label="Total Residents" value={kpis.total_residents} subtitle="Active lease holders" color={EMERALD} />
      </div>

      <hr className="border-[var(--border)]" />

      {/* ── OCCUPANCY ── */}
      <SectionHeader label="OCCUPANCY" title="Occupancy Rate by Property" subtitle="Sorted from lowest to highest - red indicates properties needing attention." color={CYAN_DEEP} />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className={`lg:col-span-2 ${CHART_CARD}`}>
          <ResponsiveContainer width="100%" height={Math.max(400, occupancy.length * 32)}>
            <BarChart data={occupancy} layout="vertical" margin={{ left: 140, right: 40, top: 10, bottom: 10 }}>
              <XAxis type="number" domain={[0, 110]} tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
              <YAxis type="category" dataKey="property" tick={{ fill: FOREGROUND, fontSize: 11 }} width={130} />
              <Tooltip {...tooltipStyle} formatter={(v) => [`${v}%`, "Occupancy"]} />
              <Bar dataKey="occupancy" radius={[0, 6, 6, 0]} label={{ position: "right", fill: FOREGROUND, fontSize: 11, formatter: (v: unknown) => `${v}%` }}>
                {occupancy.map((entry, i) => (
                  <Cell key={i} fill={occColor(entry.occupancy)} fillOpacity={0.85} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        {/* Radial bar - top properties */}
        <div className={CHART_CARD}>
          <p className="text-xs font-bold text-[var(--muted)] uppercase tracking-wider mb-3">Top Properties</p>
          <ResponsiveContainer width="100%" height={380}>
            <RadialBarChart innerRadius="20%" outerRadius="90%" data={occupancyRadial} startAngle={180} endAngle={0}>
              <RadialBar dataKey="occupancy" background={{ fill: "#f3f4f6" }} cornerRadius={6} label={{ position: "insideStart", fill: "#fff", fontSize: 10 }} />
              <Legend iconSize={8} wrapperStyle={{ fontSize: 11, color: FOREGROUND }} />
              <Tooltip {...tooltipStyle} />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── VACANCY ── */}
      <SectionHeader label="VACANCY" title="Vacancy Analysis" subtitle="Properties with vacant units and overall portfolio unit breakdown." color={ROSE} />
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className={`lg:col-span-3 ${CHART_CARD}`}>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={vacancy_bar} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
              <XAxis dataKey="property" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} />
              <Tooltip {...tooltipStyle} />
              <Bar dataKey="vacant_rented" stackId="a" fill={EMERALD} fillOpacity={0.85} name="Vacant (Rented)" />
              <Bar dataKey="vacant_unrented" stackId="a" fill={ROSE} fillOpacity={0.85} name="Vacant (Unrented)" radius={[6, 6, 0, 0]} />
              <Legend verticalAlign="top" wrapperStyle={{ color: FOREGROUND, fontSize: 12 }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className={`lg:col-span-2 ${CHART_CARD} flex items-center justify-center`}>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie data={vacancy_pie} innerRadius={70} outerRadius={110} dataKey="value" label={({ percent }) => `${((percent ?? 0) * 100).toFixed(0)}%`} labelLine={false}>
                {vacancy_pie.map((_, i) => (
                  <Cell key={i} fill={[CYAN_DEEP, EMERALD, ROSE, ORANGE][i]} />
                ))}
              </Pie>
              <Tooltip {...tooltipStyle} />
              <Legend wrapperStyle={{ color: FOREGROUND, fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── RENT ── */}
      <SectionHeader label="RENT" title="Average Rent by Property" subtitle="Average monthly rent across all unit types per property." color={MAGENTA} />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className={CHART_CARD}>
          <p className="text-xs font-bold text-[var(--muted)] uppercase tracking-wider mb-3">Bar View</p>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={rent} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
              <XAxis dataKey="property" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `$${v.toLocaleString()}`} />
              <Tooltip {...tooltipStyle} formatter={(v) => [`$${Number(v).toLocaleString()}`, "Avg Rent"]} />
              <Bar dataKey="avg_rent" fill={MAGENTA} fillOpacity={0.85} radius={[6, 6, 0, 0]}
                label={{ position: "top", fill: FOREGROUND, fontSize: 10, formatter: (v: unknown) => `$${Number(v).toLocaleString()}` }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        {/* NEW: Rent vs Security Deposit comparison */}
        <div className={CHART_CARD}>
          <p className="text-xs font-bold text-[var(--muted)] uppercase tracking-wider mb-3">Rent vs Security Deposit</p>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={rentVsDeposit} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
              <XAxis dataKey="property" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `$${v.toLocaleString()}`} />
              <Tooltip {...tooltipStyle} formatter={(v) => [`$${Number(v).toLocaleString()}`]} />
              <Bar dataKey="avg_rent" fill={CYAN} fillOpacity={0.85} name="Avg Rent" radius={[6, 6, 0, 0]} />
              <Bar dataKey="security_deposit" fill={ORANGE} fillOpacity={0.85} name="Security Deposit" radius={[6, 6, 0, 0]} />
              <Legend verticalAlign="top" wrapperStyle={{ color: FOREGROUND, fontSize: 12 }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── REVENUE ── */}
      <SectionHeader label="REVENUE" title="Revenue by Charge Code" subtitle="Total revenue collected per charge type. Rent shown separately." color={EMERALD} />
      <div className="flex gap-4 mb-6 flex-wrap">
        <KpiCard label="Total Rent Revenue" value={`$${revenue.total_rent.toLocaleString(undefined, { maximumFractionDigits: 0 })}`} subtitle="From RENT charge code" color={EMERALD} />
        <KpiCard label="Other Revenue" value={`$${revenue.total_other.toLocaleString(undefined, { maximumFractionDigits: 0 })}`} subtitle="Parking, amenity, pet fees, etc." color={BLUE} />
        <KpiCard label="Total Concessions" value={`$${revenue.total_concessions.toLocaleString(undefined, { maximumFractionDigits: 0 })}`} subtitle="Discounts and credits given" color={ROSE} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className={CHART_CARD}>
          <p className="text-xs font-bold text-[var(--muted)] uppercase tracking-wider mb-3">Secondary Revenue Sources</p>
          <ResponsiveContainer width="100%" height={380}>
            <BarChart data={revenue.positive} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
              <XAxis dataKey="charge_code" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `$${v.toLocaleString()}`} />
              <Tooltip {...tooltipStyle} formatter={(v) => [`$${Number(v).toLocaleString()}`, "Revenue"]} />
              <Bar dataKey="amount" fill={BLUE} fillOpacity={0.85} radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className={CHART_CARD}>
          <p className="text-xs font-bold text-[var(--muted)] uppercase tracking-wider mb-3">Concessions & Credits</p>
          <ResponsiveContainer width="100%" height={380}>
            <AreaChart data={revenue.negative} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
              <defs>
                <linearGradient id="roseGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={ROSE} stopOpacity={0.4} />
                  <stop offset="100%" stopColor={ROSE} stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <XAxis dataKey="charge_code" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `$${v.toLocaleString()}`} />
              <Tooltip {...tooltipStyle} formatter={(v) => [`$${Number(v).toLocaleString()}`, "Concession"]} />
              <Area type="monotone" dataKey="amount" stroke={ROSE} fill="url(#roseGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── PIPELINE ── */}
      <SectionHeader label="PIPELINE" title="Future Applicants by Property" subtitle="Number of future residents and applicants waiting to move in per property." color={ORANGE} />
      <div className={CHART_CARD}>
        <ResponsiveContainer width="100%" height={380}>
          <BarChart data={pipelineWithColor} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
            <XAxis dataKey="property" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
            <YAxis tick={{ fill: MUTED, fontSize: 11 }} />
            <Tooltip {...tooltipStyle} />
            <Bar dataKey="applicants" radius={[6, 6, 0, 0]}
              label={{ position: "top", fill: FOREGROUND, fontSize: 11 }}>
              {pipelineWithColor.map((entry, i) => (
                <Cell key={i} fill={entry.fill} fillOpacity={0.85} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── DEPOSITS ── */}
      <SectionHeader label="DEPOSITS" title="Security Deposits by Property" subtitle="Total security deposits held per property for current and notice residents." color={BLUE} />
      <div className={CHART_CARD}>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={deposits} margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
            <XAxis dataKey="property" tick={{ fill: FOREGROUND, fontSize: 10 }} angle={-35} textAnchor="end" />
            <YAxis tick={{ fill: MUTED, fontSize: 11 }} tickFormatter={(v) => `$${v.toLocaleString()}`} />
            <Tooltip {...tooltipStyle} formatter={(v) => [`$${Number(v).toLocaleString()}`]} />
            <Bar dataKey="security_deposit" stackId="a" fill={CYAN_DEEP} fillOpacity={0.85} name="Security Deposit" />
            <Bar dataKey="other_deposits" stackId="a" fill={LIME} fillOpacity={0.85} name="Other Deposits" radius={[6, 6, 0, 0]} />
            <Legend verticalAlign="top" wrapperStyle={{ color: FOREGROUND, fontSize: 12 }} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <hr className="border-[var(--border)] mt-8" />

      {/* ── LEASE EXPIRATIONS ── */}
      <SectionHeader label="LEASE EXPIRATIONS" title="Upcoming Expirations - Next 90 Days" subtitle={`${lease_expirations.length} lease${lease_expirations.length !== 1 ? "s" : ""} expiring in the next 90 days`} color={ORANGE} />
      {lease_expirations.length > 0 ? (
        <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Resident</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Unit</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Expires On</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Property</th>
                </tr>
              </thead>
              <tbody>
                {lease_expirations.map((row, i) => (
                  <tr key={i} className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors">
                    <td className="px-4 py-2 text-[13px] text-[var(--foreground)] font-medium">{row.name}</td>
                    <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{row.unit}</td>
                    <td className="px-4 py-2 text-[13px] font-semibold" style={{ color: ORANGE }}>{row.expiration}</td>
                    <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{row.property}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <p className="text-sm text-[var(--muted)]">No leases expiring in the next 90 days.</p>
      )}

      <hr className="border-[var(--border)] mt-8" />

      {/* ── OUTSTANDING BALANCES ── */}
      <SectionHeader label="OUTSTANDING BALANCES" title="Residents with a Balance Owing" subtitle={`${outstanding_balances.length} resident${outstanding_balances.length !== 1 ? "s" : ""} with an outstanding balance`} color={ROSE} />
      {outstanding_balances.length > 0 ? (
        <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden shadow-sm mb-8">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Resident</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Unit</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Balance Owing</th>
                  <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Property</th>
                </tr>
              </thead>
              <tbody>
                {outstanding_balances.map((row, i) => (
                  <tr key={i} className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors">
                    <td className="px-4 py-2 text-[13px] text-[var(--foreground)] font-medium">{row.name}</td>
                    <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{row.unit}</td>
                    <td className="px-4 py-2 text-[13px] font-bold" style={{ color: ROSE }}>${row.balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                    <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{row.property}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <p className="text-sm text-[var(--muted)] mb-8">No residents with outstanding balances.</p>
      )}
    </div>
  );
}
