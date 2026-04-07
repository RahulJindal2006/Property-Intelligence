import Image from "next/image";

const HOW_IT_WORKS = [
  { icon: "🧠", title: "Intent Classification", text: "The AI first determines whether your message is a data question or casual conversation before generating any SQL.", color: "var(--cyan-deep)" },
  { icon: "⚡", title: "SQL Generation", text: "A prompt-engineered LangChain template converts natural language into precise SQLite queries with built-in safety rules.", color: "var(--magenta)" },
  { icon: "🛡️", title: "Safety Layer", text: "All destructive operations (DROP, DELETE, UPDATE) are blocked at the execution layer before any query reaches the database.", color: "var(--rose)" },
  { icon: "📊", title: "Live Data Tables", text: "Results are returned as interactive tables alongside a plain-English summary of what the data shows.", color: "var(--lime)" },
  { icon: "🔍", title: "SQL Transparency", text: "Every data response includes a toggleable SQL query view so technical users can verify exactly what was run.", color: "var(--orange)" },
  { icon: "🚨", title: "Issue Reporting", text: "Users can flag incorrect responses with severity levels. Reports are stored and reviewed via a password-protected admin panel.", color: "var(--blue)" },
];

const TECH_STACK = [
  { tag: "Python", color: "var(--cyan-deep)", desc: "Backend logic & ETL pipeline" },
  { tag: "FastAPI", color: "var(--lime)", desc: "REST API framework" },
  { tag: "Next.js", color: "var(--foreground)", desc: "React meta-framework" },
  { tag: "React", color: "var(--cyan-deep)", desc: "Component-based UI" },
  { tag: "TypeScript", color: "var(--blue)", desc: "Type-safe frontend" },
  { tag: "Tailwind CSS", color: "var(--cyan-deep)", desc: "Utility-first styling" },
  { tag: "LangChain", color: "var(--magenta)", desc: "LLM orchestration layer" },
  { tag: "OpenAI GPT-3.5", color: "var(--lime)", desc: "Natural language model" },
  { tag: "SQLite", color: "var(--orange)", desc: "Lightweight database engine" },
  { tag: "Pandas", color: "var(--blue)", desc: "Data transformation" },
  { tag: "Recharts", color: "var(--rose)", desc: "Interactive chart library" },
  { tag: "Prompt Engineering", color: "var(--magenta)", desc: "70+ SQL examples" },
  { tag: "NL to SQL", color: "var(--cyan-deep)", desc: "Natural language queries" },
  { tag: "ETL Pipeline", color: "var(--orange)", desc: "Excel to database ingestion" },
];

const DB_TABLES = [
  { name: "lease_charges", rows: "7,400+", desc: "Resident, unit, rent & lease data", color: "var(--cyan-deep)" },
  { name: "property_summary", rows: "25", desc: "Occupancy, vacancy & leasing stats", color: "var(--magenta)" },
  { name: "summary_groups", rows: "1,200+", desc: "Grouped property sub-metrics", color: "var(--lime)" },
  { name: "charge_code_summary", rows: "500+", desc: "Revenue per charge code", color: "var(--orange)" },
];

export default function AboutPage() {
  return (
    <div className="p-8 w-full">
      {/* ── HERO ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 py-8 border-b border-[var(--border)] mb-10">
        {/* Left: photo + bio */}
        <div className="lg:col-span-2 flex items-start gap-6">
          <Image
            src="/Profile.png"
            alt="Rahul Jindal"
            width={110}
            height={110}
            className="rounded-full border-[3px] flex-shrink-0 object-cover shadow-lg"
            style={{ borderColor: "var(--cyan)" }}
          />
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-[var(--foreground)] mb-1">Rahul Jindal</h1>
            <div
              className="text-sm font-semibold tracking-wider mb-3"
              style={{ color: "var(--cyan-deep)" }}
            >
              CS/BBA STUDENT · WILFRID LAURIER UNIVERSITY
            </div>
            <p className="text-sm text-[var(--muted)] leading-relaxed">
              I&apos;m a Computer Science & Business Administration student at Wilfrid Laurier University with hands-on experience
              building web applications, AI-powered tools, and data platforms. In my previous software engineering position,
              I was regularly given raw Excel rent roll files and tasked with extracting data, building databases, and
              creating AI-powered SQL chatbots. This project is a replica of that work - built from scratch to demonstrate
              the full end-to-end process.
            </p>
          </div>
        </div>

        {/* Right: link buttons filling the column */}
        <div className="flex flex-col gap-3 justify-center">
          {[
            { href: "https://www.linkedin.com/in/rahuljindal-cs/", label: "LinkedIn", color: "var(--blue)", icon: "in" },
            { href: "https://github.com/RahulJindal2006", label: "GitHub", color: "var(--foreground)", icon: "<>" },
            { href: "mailto:jind3091@mylaurier.ca", label: "Email", color: "var(--magenta)", icon: "@" },
          ].map((link) => (
            <a
              key={link.label}
              href={link.href}
              target="_blank"
              className="flex items-center gap-4 px-5 py-4 rounded-xl border bg-white hover:shadow-md hover:-translate-y-0.5 transition-all"
              style={{ borderColor: link.color }}
            >
              <span
                className="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-sm flex-shrink-0"
                style={{ background: link.color }}
              >
                {link.icon}
              </span>
              <div>
                <div className="text-sm font-bold" style={{ color: link.color }}>{link.label}</div>
                <div className="text-xs text-[var(--muted)]">{link.href.replace(/^(https?:\/\/(www\.)?|mailto:)/, "")}</div>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* ── CONTEXT ── */}
      <div className="text-[11px] font-bold tracking-[0.12em] uppercase mb-4" style={{ color: "var(--cyan-deep)" }}>THE CONTEXT</div>
      <div className="flex items-center gap-5 bg-white border border-[var(--border)] rounded-2xl px-7 py-6 mb-10 shadow-sm">
        <Image
          src="/logo.svg"
          alt="Logo"
          width={60}
          height={60}
          className="rounded-xl flex-shrink-0"
        />
        <div>
          <div className="text-base font-bold text-[var(--foreground)] mb-1.5">A replica of production work</div>
          <p className="text-[13px] text-[var(--muted)] leading-relaxed">
            In my previous role as a software engineer, I was given raw Excel rent roll files and asked to extract
            as much data as possible - building CSV reports, structured databases, and ultimately AI-powered SQL chatbots
            that let non-technical team members query property data in plain English. This project recreates that
            entire pipeline end-to-end using sample data, so you can see exactly how the process works.
          </p>
        </div>
      </div>

      {/* ── HOW IT WORKS ── */}
      <div className="text-[11px] font-bold tracking-[0.12em] uppercase mb-4" style={{ color: "var(--magenta)" }}>HOW IT WORKS</div>
      <h2 className="text-2xl font-extrabold tracking-tight text-[var(--foreground)] mb-3">From question to answer in seconds</h2>
      <p className="text-sm text-[var(--muted)] leading-relaxed mb-6">
        Type any question in plain English. The AI classifies your intent, generates the correct SQL query, runs it
        against the live database, and returns a human-readable summary - all in one seamless flow.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
        {HOW_IT_WORKS.map((card) => (
          <div
            key={card.title}
            className="bg-white border border-[var(--border)] rounded-2xl px-5 py-5 hover:shadow-md hover:-translate-y-0.5 transition-all"
          >
            <div className="text-2xl mb-2.5">{card.icon}</div>
            <div className="text-sm font-bold text-[var(--foreground)] mb-1.5">{card.title}</div>
            <div className="text-[13px] text-[var(--muted)] leading-relaxed">{card.text}</div>
          </div>
        ))}
      </div>

      {/* ── TECH STACK ── */}
      <div className="text-[11px] font-bold tracking-[0.12em] uppercase mb-4" style={{ color: "var(--orange)" }}>TECH STACK</div>
      <h2 className="text-2xl font-extrabold tracking-tight text-[var(--foreground)] mb-4">Built with</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 mb-10">
        {TECH_STACK.map((t) => (
          <div
            key={t.tag}
            className="bg-white border border-[var(--border)] rounded-xl px-4 py-4 hover:shadow-md hover:-translate-y-0.5 transition-all"
          >
            <div className="text-sm font-bold mb-1" style={{ color: t.color }}>{t.tag}</div>
            <div className="text-[11px] text-[var(--muted)] leading-relaxed">{t.desc}</div>
          </div>
        ))}
      </div>

      {/* ── DATA PIPELINE ── */}
      <div className="text-[11px] font-bold tracking-[0.12em] uppercase mb-4" style={{ color: "var(--lime)" }}>DATA PIPELINE</div>
      <h2 className="text-2xl font-extrabold tracking-tight text-[var(--foreground)] mb-3">How the data gets in</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Left: description */}
        <div>
          <p className="text-sm text-[var(--muted)] leading-relaxed mb-4">
            Just like on the job, the process starts with raw Excel rent roll files. A custom ETL pipeline (<code style={{ color: "var(--cyan-deep)" }}>script.py</code>)
            ingests 50 Excel reports, cleans and standardizes the data, and loads it into four SQLite tables.
          </p>
          <p className="text-sm text-[var(--muted)] leading-relaxed">
            The pipeline handles forward-filling, date normalization,
            property ID extraction, placeholder row filtering, and charge code aggregation - replicating exactly the kind of
            data engineering work I did professionally.
          </p>
        </div>

        {/* Right: table cards */}
        <div className="grid grid-cols-2 gap-3">
          {DB_TABLES.map((table) => (
            <div
              key={table.name}
              className="bg-white border border-[var(--border)] rounded-xl px-4 py-4 hover:shadow-md transition-all"
            >
              <div className="text-xs font-bold font-mono mb-1" style={{ color: table.color }}>{table.name}</div>
              <div className="text-lg font-extrabold text-[var(--foreground)] mb-0.5">{table.rows}</div>
              <div className="text-[11px] text-[var(--muted)]">{table.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
