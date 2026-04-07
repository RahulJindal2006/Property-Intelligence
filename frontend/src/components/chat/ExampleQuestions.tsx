const EXAMPLES = [
  { q: "How many vacant units do we have?", color: "var(--cyan)" },
  { q: "Which properties have the lowest occupancy?", color: "var(--magenta)" },
  { q: "Show me residents with a balance", color: "var(--lime)" },
  { q: "What is our average rent?", color: "var(--orange)" },
  { q: "Which leases expire in 90 days?", color: "var(--rose)" },
  { q: "How many total residents do we have?", color: "var(--blue)" },
];

interface Props {
  onSelect: (question: string) => void;
}

export default function ExampleQuestions({ onSelect }: Props) {
  return (
    <div>
      <div className="text-[11px] font-bold tracking-[0.15em] text-[var(--muted)] uppercase mb-3">
        Try Asking
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
        {EXAMPLES.map((ex) => (
          <button
            key={ex.q}
            onClick={() => onSelect(ex.q)}
            className="text-left px-4 py-3 text-[13px] font-medium rounded-xl border border-[var(--border)] bg-white hover:shadow-md hover:-translate-y-0.5 transition-all group"
          >
            <span
              className="inline-block w-1.5 h-1.5 rounded-full mr-2 group-hover:scale-150 transition-transform"
              style={{ background: ex.color }}
            />
            {ex.q}
          </button>
        ))}
      </div>
    </div>
  );
}
