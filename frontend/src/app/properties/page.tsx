"use client";

import { useEffect, useState } from "react";
import { getPropertiesOverview } from "@/lib/api";
import type { PropertiesData } from "@/lib/types";
import PageHeader from "@/components/layout/PageHeader";

const CHARGE_CODES: Record<string, [string, string][]> = {
  "Revenue Charges": [
    ["RENT", "Standard monthly rent charge for the unit"],
    ["RENTAFF", "Affordable housing rent - reduced rate for income-qualified residents"],
    ["RENTRETL", "Retail unit rent - charged for commercial/retail spaces"],
    ["RNTPROF", "Professional or corporate rent rate"],
    ["RENTHAP", "Housing assistance program rent - subsidized rent rate"],
    ["MTM", "Month-to-month premium - extra charge for residents on a month-to-month lease"],
  ],
  "Amenity & Unit Charges": [
    ["AMENITY", "Monthly amenity fee for access to shared building amenities"],
    ["PARKING", "Monthly parking space charge"],
    ["GARAGE", "Monthly garage unit charge"],
    ["STORAGE", "Monthly storage unit charge"],
    ["BIKE", "Monthly bike storage charge"],
    ["W/D", "Washer/dryer unit charge"],
    ["HOMEPCKG", "Home package bundle - includes multiple amenities or services"],
  ],
  "Utility & Fee Charges": [
    ["PETFEEM", "Monthly pet fee for residents with pets"],
    ["PETFEE", "One-time or alternative pet fee"],
    ["TRASH", "Monthly trash/waste removal fee"],
    ["WATER", "Monthly water utility charge"],
    ["UTILCOM", "Common area utility charge"],
    ["SDFEE", "Same-day or service delivery fee"],
    ["SALESTX", "Sales tax applied to applicable charges"],
    ["CAMEST", "Common area maintenance estimate charge"],
    ["CAMINSR", "Common area maintenance insurance charge"],
    ["RETXEST", "Real estate tax estimate charge passed through to resident"],
  ],
  "Subsidies & Credits": [
    ["SUBSIDY", "Government or program subsidy applied to resident account"],
    ["SEC8CRD", "Section 8 housing voucher credit - government housing assistance"],
  ],
  "Concessions (Negative Charges)": [
    ["CONRENT", "Rent concession - discount applied to monthly rent"],
    ["CONPARK", "Parking concession - free or discounted parking offered as incentive"],
    ["CONGAR", "Garage concession - free or discounted garage unit"],
    ["CONSTOR", "Storage concession - free or discounted storage unit"],
    ["CONPETM", "Pet fee concession - waived or reduced pet fee"],
    ["CONAMEN", "Amenity concession - waived or discounted amenity fee"],
    ["CONEMP", "Employee concession - discounted rent for property staff living on-site"],
  ],
};

const CATEGORY_COLORS: Record<string, string> = {
  "Revenue Charges": "var(--cyan-deep)",
  "Amenity & Unit Charges": "var(--magenta)",
  "Utility & Fee Charges": "var(--orange)",
  "Subsidies & Credits": "var(--lime)",
  "Concessions (Negative Charges)": "var(--rose)",
};

export default function PropertiesPage() {
  const [data, setData] = useState<PropertiesData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPropertiesOverview()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-[var(--muted)]">Loading...</div>;
  if (!data) return <div className="p-8" style={{ color: "var(--rose)" }}>Failed to load data.</div>;

  const { metrics, properties_table, charge_codes_table, deposits_table } = data;

  const metricCards = [
    { label: "Total Properties", value: Math.round(metrics.total_props), color: "var(--cyan-deep)" },
    { label: "Total Units", value: Math.round(metrics.total_units), color: "var(--magenta)" },
    { label: "Avg Occupancy", value: `${metrics.avg_occ}%`, color: "var(--lime)" },
    { label: "Total Vacant", value: Math.round(metrics.total_vacant), color: "var(--rose)" },
    { label: "Future Applicants", value: Math.round(metrics.total_future), color: "var(--orange)" },
    { label: "Security Deposits", value: `$${Math.round(metrics.total_deposits).toLocaleString()}`, color: "var(--blue)" },
  ];

  return (
    <div className="p-8 w-full">
      <PageHeader label="PORTFOLIO" title="Property Overview" subtitle="A live summary of all your properties pulled directly from the database." color="var(--magenta)" />

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {metricCards.map((m) => (
          <div key={m.label} className="bg-white border border-[var(--border)] rounded-xl px-4 py-4 text-center shadow-sm hover:shadow-md transition-shadow">
            <div className="text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase mb-1">{m.label}</div>
            <div className="text-xl font-extrabold" style={{ color: m.color }}>{m.value}</div>
          </div>
        ))}
      </div>

      <hr className="border-[var(--border)] mb-8" />

      {/* All Properties Table */}
      <h2 className="text-xl font-extrabold mb-1 text-[var(--foreground)]">All Properties</h2>
      <p className="text-[13px] text-[var(--muted)] mb-4">Sorted by occupancy. Grouped by property name across buildings.</p>
      <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden shadow-sm mb-8">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
                {["Property", "Total Units", "Occupied", "Vacant (Rented)", "Vacant (Unrented)", "Available", "Occupancy %", "Leased %", "Trend %"].map((h) => (
                  <th key={h} className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {properties_table.map((row, i) => (
                <tr key={i} className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors">
                  <td className="px-4 py-2 text-[13px] font-medium text-[var(--foreground)]">{String(row.Property_Name)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Total_Units)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Occupied)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Vacant_Rented)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Vacant_Unrented)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Available_Units)}</td>
                  <td className="px-4 py-2 text-[13px] font-semibold" style={{ color: "var(--cyan-deep)" }}>{String(row.Occupancy_Pct)}%</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Leased_Pct)}%</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Trend_Pct)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <hr className="border-[var(--border)] mb-8" />

      {/* Revenue by Charge Code */}
      <h2 className="text-xl font-extrabold mb-1 text-[var(--foreground)]">Revenue by Charge Code</h2>
      <p className="text-[13px] text-[var(--muted)] mb-4">Total revenue collected per charge type across all properties.</p>
      <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden shadow-sm mb-8">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Charge Code</th>
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Total Revenue ($)</th>
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Properties</th>
              </tr>
            </thead>
            <tbody>
              {charge_codes_table.map((row, i) => (
                <tr key={i} className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors">
                  <td className="px-4 py-2 text-[13px] font-mono font-bold text-[var(--foreground)]">{String(row.Charge_Code)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">${Number(row.Total_Revenue).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">{String(row.Properties)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <hr className="border-[var(--border)] mb-8" />

      {/* Security Deposits */}
      <h2 className="text-xl font-extrabold mb-1 text-[var(--foreground)]">Security Deposits by Property</h2>
      <p className="text-[13px] text-[var(--muted)] mb-4">Total security deposits held per property for current and notice residents.</p>
      <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden shadow-sm mb-8">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Property</th>
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Security Deposit ($)</th>
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Other Deposits ($)</th>
                <th className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase">Total Deposits ($)</th>
              </tr>
            </thead>
            <tbody>
              {deposits_table.map((row, i) => (
                <tr key={i} className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors">
                  <td className="px-4 py-2 text-[13px] font-medium text-[var(--foreground)]">{String(row.Property_Name)}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">${Number(row.Total_Security_Deposit).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                  <td className="px-4 py-2 text-[13px] text-[var(--muted)]">${Number(row.Total_Other_Deposits).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                  <td className="px-4 py-2 text-[13px] font-semibold" style={{ color: "var(--cyan-deep)" }}>${Number(row.Total_Deposits).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <hr className="border-[var(--border)] mb-8" />

      {/* Charge Code Reference */}
      <h2 className="text-xl font-extrabold mb-1 text-[var(--foreground)]">Charge Code Reference</h2>
      <p className="text-[13px] text-[var(--muted)] mb-6">Definitions for all charge codes used across properties.</p>
      {Object.entries(CHARGE_CODES).map(([category, codes]) => (
        <div key={category} className="mb-6">
          <div
            className="text-[11px] font-bold tracking-[0.12em] uppercase mb-3"
            style={{ color: CATEGORY_COLORS[category] || "var(--cyan-deep)" }}
          >
            {category}
          </div>
          <div className="space-y-2">
            {codes.map(([code, desc]) => (
              <div
                key={code}
                className="bg-white border border-[var(--border)] rounded-xl px-4 py-3 flex items-center justify-between gap-4 hover:shadow-sm transition-shadow"
              >
                <span className="text-[13px] font-bold font-mono min-w-[100px] text-[var(--foreground)]">{code}</span>
                <span className="text-[13px] text-[var(--muted)] flex-1">{desc}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
