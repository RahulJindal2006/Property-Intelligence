"use client";

import Image from "next/image";
import Link from "next/link";

const STATS = [
  { value: "25", label: "Properties", color: "var(--cyan)" },
  { value: "9,100+", label: "Lease Records", color: "var(--magenta)" },
  { value: "4", label: "Data Tables", color: "var(--lime)" },
  { value: "50", label: "Source Files", color: "var(--orange)" },
];

const FEATURES = [
  {
    icon: "💬",
    title: "Natural Language SQL",
    desc: "Ask questions in plain English. The AI translates your words into precise SQL queries and returns instant, human-readable answers.",
    gradient: "var(--gradient-cyan)",
    color: "var(--cyan)",
  },
  {
    icon: "📊",
    title: "Interactive Dashboards",
    desc: "Explore occupancy trends, revenue breakdowns, vacancy analysis, and more through beautiful, interactive visualizations.",
    gradient: "var(--gradient-magenta)",
    color: "var(--magenta)",
  },
  {
    icon: "🛡️",
    title: "Safe & Transparent",
    desc: "Every query is protected by a safety layer that blocks destructive operations. View the exact SQL behind every answer.",
    gradient: "var(--gradient-lime)",
    color: "var(--lime)",
  },
  {
    icon: "⚡",
    title: "Real-Time Data",
    desc: "Powered by a live SQLite database built from 50 Excel reports - covering rent rolls, availability, charges, and deposits.",
    gradient: "var(--gradient-warm)",
    color: "var(--orange)",
  },
];

const PIPELINE_STEPS = [
  { step: "01", title: "Extract", desc: "50 raw Excel rent roll files - the same format I received on the job", color: "var(--cyan)" },
  { step: "02", title: "Transform", desc: "Clean, standardize, and normalize into structured data", color: "var(--magenta)" },
  { step: "03", title: "Load", desc: "Populate 4 SQLite tables with 9,100+ records", color: "var(--lime)" },
  { step: "04", title: "Query", desc: "AI converts plain English into SQL and returns insights", color: "var(--orange)" },
];

export default function LandingPage() {
  return (
    <main className="w-full">
      {/* ============ HERO SECTION ============ */}
      <section className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-20 blur-3xl" style={{ background: "var(--cyan)" }} />
          <div className="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-15 blur-3xl" style={{ background: "var(--magenta)" }} />
          <div className="absolute top-1/3 left-1/2 w-64 h-64 rounded-full opacity-10 blur-3xl" style={{ background: "var(--orange)" }} />
        </div>

        {/* Top nav */}
        <nav className="absolute top-0 left-0 right-0 flex items-center justify-between px-8 py-5">
          <div className="flex items-center gap-3">
            <Image src="/logo.svg" alt="Rahul Jindal" width={36} height={36} className="rounded-full" />
            <span className="text-sm font-bold tracking-wide">Property Intelligence</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/about" className="text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors font-medium">
              About
            </Link>
            <Link
              href="/chat"
              className="text-sm font-semibold text-white px-5 py-2 rounded-full transition-all hover:scale-105 hover:shadow-lg"
              style={{ background: "var(--gradient-cyan)" }}
            >
              Launch App
            </Link>
          </div>
        </nav>

        {/* Hero content */}
        <div className="relative z-10 text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--border)] bg-white/80 backdrop-blur-sm mb-8 shadow-sm">
            <span className="w-2 h-2 rounded-full animate-pulse" style={{ background: "var(--emerald)" }} />
            <span className="text-xs font-semibold text-[var(--muted)]">Powered by GPT-3.5 + LangChain</span>
          </div>

          <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6">
            Understand Your{" "}
            <span className="text-gradient">Community</span>
          </h1>

          <p className="text-lg md:text-xl text-[var(--muted)] leading-relaxed max-w-2xl mx-auto mb-10">
            A full-stack AI platform that takes raw Excel rent rolls, builds a structured database, and lets you
            query property data in plain English. Built as a replica of my professional engineering work.
          </p>

          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Link
              href="/chat"
              className="inline-flex items-center gap-2 text-base font-bold text-white px-8 py-4 rounded-2xl transition-all hover:scale-105 hover:shadow-xl shadow-lg"
              style={{ background: "var(--gradient-cyan)" }}
            >
              Get Started
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 text-base font-bold text-[var(--foreground)] px-8 py-4 rounded-2xl border-2 border-[var(--border)] hover:border-[var(--magenta)] hover:text-[var(--magenta-deep)] transition-all"
            >
              View Dashboards
            </Link>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--dimmed)" strokeWidth="2" strokeLinecap="round">
            <path d="M12 5v14M5 12l7 7 7-7" />
          </svg>
        </div>
      </section>

      {/* ============ STATS BAR ============ */}
      <section className="py-16 border-y border-[var(--border)] bg-[var(--surface)]">
        <div className="max-w-5xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {STATS.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-4xl font-extrabold tracking-tight mb-1" style={{ color: stat.color }}>
                  {stat.value}
                </div>
                <div className="text-sm font-medium text-[var(--muted)]">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============ ABOUT THE PROJECT ============ */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-[11px] font-bold tracking-[0.2em] uppercase mb-3" style={{ color: "var(--magenta)" }}>
              The Backstory
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-6">
              Built From Real Experience
            </h2>
            <p className="text-lg text-[var(--muted)] leading-relaxed max-w-2xl mx-auto">
              In my previous software engineering role, I was regularly handed raw Excel rent roll files
              and tasked with <strong className="text-[var(--foreground)]">extracting as much data as possible, building structured
              databases, generating CSV reports, and creating AI-powered SQL chatbots</strong> to make that data accessible.
              This project is a replica of that exact workflow - built from scratch to demonstrate how it&apos;s done.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold text-sm" style={{ background: "var(--cyan)" }}>
                  01
                </div>
                <div>
                  <h3 className="font-bold mb-1">The Real-World Task</h3>
                  <p className="text-sm text-[var(--muted)] leading-relaxed">
                    On the job, I&apos;d receive Excel rent roll exports containing thousands of rows - lease data,
                    charge codes, occupancy stats, and deposit records across dozens of properties.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold text-sm" style={{ background: "var(--magenta)" }}>
                  02
                </div>
                <div>
                  <h3 className="font-bold mb-1">The Engineering Process</h3>
                  <p className="text-sm text-[var(--muted)] leading-relaxed">
                    I built ETL pipelines to clean and normalize the data, loaded it into structured SQLite databases,
                    and then created AI chatbots that let anyone query the data in plain English - no SQL required.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold text-sm" style={{ background: "var(--lime-deep)" }}>
                  03
                </div>
                <div>
                  <h3 className="font-bold mb-1">This Replica</h3>
                  <p className="text-sm text-[var(--muted)] leading-relaxed">
                    This project recreates that entire end-to-end workflow using sample property data - from
                    raw Excel ingestion to a full-stack AI chatbot with dashboards and analytics.
                  </p>
                </div>
              </div>
            </div>

            {/* Visual card */}
            <div className="relative">
              <div className="absolute inset-0 rounded-3xl opacity-10 blur-2xl" style={{ background: "var(--gradient-hero)" }} />
              <div className="relative bg-white rounded-3xl border border-[var(--border)] p-8 shadow-xl">
                <div className="flex items-center gap-3 mb-6">
                  <Image src="/logo.svg" alt="Rahul Jindal" width={44} height={44} className="rounded-full" />
                  <div>
                    <div className="font-bold">Property Intelligence</div>
                    <div className="text-xs text-[var(--muted)]">End-to-End Data Pipeline + AI Chatbot</div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="bg-[var(--surface)] rounded-xl p-3">
                    <div className="text-xs text-[var(--muted)] mb-1">You asked:</div>
                    <div className="text-sm font-medium">&quot;How many vacant units do we have?&quot;</div>
                  </div>
                  <div className="rounded-xl p-3 text-white" style={{ background: "var(--gradient-cyan)" }}>
                    <div className="text-xs opacity-80 mb-1">AI Response:</div>
                    <div className="text-sm font-medium">You currently have 47 vacant units across all 25 properties in the portfolio.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ FEATURES ============ */}
      <section className="py-24 px-6 bg-[var(--surface)]">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-[11px] font-bold tracking-[0.2em] uppercase mb-3" style={{ color: "var(--cyan-deep)" }}>
              Capabilities
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
              What It Can Do
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {FEATURES.map((f) => (
              <div
                key={f.title}
                className="bg-white rounded-2xl border border-[var(--border)] p-7 hover:shadow-lg transition-all hover:-translate-y-1 group"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-4 transition-transform group-hover:scale-110"
                  style={{ background: `${f.color}15` }}
                >
                  {f.icon}
                </div>
                <h3 className="text-lg font-bold mb-2">{f.title}</h3>
                <p className="text-sm text-[var(--muted)] leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============ DATA PIPELINE ============ */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-[11px] font-bold tracking-[0.2em] uppercase mb-3" style={{ color: "var(--orange)" }}>
              Data Pipeline
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
              From Excel to Insights
            </h2>
            <p className="text-lg text-[var(--muted)] max-w-xl mx-auto">
              A custom ETL pipeline processes raw property data into a queryable database.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            {PIPELINE_STEPS.map((s) => (
              <div key={s.step} className="text-center">
                <div
                  className="w-14 h-14 rounded-2xl flex items-center justify-center text-white font-extrabold text-lg mx-auto mb-4"
                  style={{ background: s.color }}
                >
                  {s.step}
                </div>
                <h3 className="font-bold mb-1">{s.title}</h3>
                <p className="text-sm text-[var(--muted)] leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============ CTA ============ */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="relative">
            <div className="absolute inset-0 rounded-3xl opacity-10 blur-3xl" style={{ background: "var(--gradient-hero)" }} />
            <div className="relative bg-white rounded-3xl border border-[var(--border)] px-12 py-16 shadow-xl">
              <h2 className="text-4xl font-extrabold tracking-tight mb-4">
                Ready to Explore?
              </h2>
              <p className="text-lg text-[var(--muted)] mb-8 max-w-md mx-auto">
                Start asking questions about your properties and get instant, AI-powered answers.
              </p>
              <div className="flex items-center justify-center gap-4 flex-wrap">
                <Link
                  href="/chat"
                  className="inline-flex items-center gap-2 text-base font-bold text-white px-8 py-4 rounded-2xl transition-all hover:scale-105 hover:shadow-xl shadow-lg"
                  style={{ background: "var(--gradient-cyan)" }}
                >
                  Open AI Chat
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </Link>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 text-base font-bold px-8 py-4 rounded-2xl border-2 border-[var(--border)] hover:border-[var(--magenta)] hover:text-[var(--magenta-deep)] transition-all"
                >
                  View Dashboards
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ FOOTER ============ */}
      <footer className="py-8 px-6 border-t border-[var(--border)]">
        <div className="max-w-5xl mx-auto flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <Image src="/logo.svg" alt="Rahul Jindal" width={28} height={28} className="rounded-full" />
            <span className="text-sm font-semibold text-[var(--muted)]">Property Intelligence</span>
          </div>
          <div className="text-xs text-[var(--dimmed)]">
            Built by Rahul Jindal - CS/BBA @ Wilfrid Laurier University
          </div>
          <div className="flex gap-4">
            <Link href="/schema" className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors">Schema</Link>
            <Link href="/issues" className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors">Issues</Link>
            <Link href="/about" className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors">About</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
