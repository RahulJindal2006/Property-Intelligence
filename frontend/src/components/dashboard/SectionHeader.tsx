interface Props {
  label: string;
  title: string;
  subtitle: string;
  color?: string;
}

export default function SectionHeader({ label, title, subtitle, color }: Props) {
  return (
    <div className="mt-10 mb-5">
      <div
        className="text-[11px] font-bold tracking-[0.12em] uppercase mb-2"
        style={{ color: color || "var(--cyan-deep)" }}
      >
        {label}
      </div>
      <h2 className="text-xl font-extrabold tracking-tight text-[var(--foreground)] mb-1">{title}</h2>
      <p className="text-[13px] text-[var(--muted)]">{subtitle}</p>
    </div>
  );
}
