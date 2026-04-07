interface Props {
  label: string;
  value: string | number;
  subtitle: string;
  color?: string;
}

export default function KpiCard({ label, value, subtitle, color }: Props) {
  return (
    <div className="flex-1 min-w-[180px] bg-white border border-[var(--border)] rounded-2xl px-6 py-5 text-center shadow-sm hover:shadow-md transition-shadow">
      <div className="text-[11px] font-bold tracking-[0.12em] text-[var(--muted)] uppercase mb-2">
        {label}
      </div>
      <div
        className="text-3xl font-extrabold tracking-tight mb-1"
        style={{ color: color || "var(--foreground)" }}
      >
        {typeof value === "number" ? value.toLocaleString() : value}
      </div>
      <div className="text-[11px] text-[var(--muted)]">{subtitle}</div>
    </div>
  );
}
