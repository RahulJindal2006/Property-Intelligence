interface PageHeaderProps {
  label: string;
  title: string;
  subtitle: string;
  color?: string;
}

export default function PageHeader({ label, title, subtitle, color }: PageHeaderProps) {
  return (
    <div className="pb-6 border-b border-[var(--border)] mb-8">
      <div
        className="text-[11px] font-bold tracking-[0.15em] uppercase mb-1.5"
        style={{ color: color || "var(--cyan-deep)" }}
      >
        {label}
      </div>
      <h1 className="text-3xl font-extrabold tracking-tight text-[var(--foreground)] mb-1.5">
        {title}
      </h1>
      <p className="text-sm text-[var(--muted)]">{subtitle}</p>
    </div>
  );
}
