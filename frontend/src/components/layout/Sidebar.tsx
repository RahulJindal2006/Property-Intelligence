"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";

const navItems = [
  { href: "/chat", label: "AI Chat", icon: "💬", color: "var(--cyan)" },
  { href: "/dashboard", label: "Dashboard", icon: "📊", color: "var(--magenta)" },
  { href: "/properties", label: "Properties", icon: "🏢", color: "var(--lime)" },
  { href: "/schema", label: "Schema", icon: "🗄️", color: "var(--orange)" },
  { href: "/about", label: "About", icon: "ℹ️", color: "var(--blue)" },
  { href: "/issues", label: "Issues", icon: "🚨", color: "var(--rose)" },
];

interface SidebarProps {
  open: boolean;
  onToggle: () => void;
}

export default function Sidebar({ open, onToggle }: SidebarProps) {
  const pathname = usePathname();

  // Hide sidebar entirely on landing page
  if (pathname === "/") return null;

  return (
    <>
      {/* Hamburger toggle - only visible when sidebar is closed */}
      {!open && (
        <button
          onClick={onToggle}
          className="fixed top-4 left-4 z-50 bg-white border border-[var(--border)] rounded-xl p-2.5 shadow-sm text-sm hover:shadow-md transition-shadow"
          aria-label="Open sidebar"
        >
          ☰
        </button>
      )}

      {/* Overlay on mobile */}
      {open && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden"
          onClick={onToggle}
        />
      )}

      <aside
        className={`fixed top-0 left-0 h-full z-40 flex flex-col bg-white border-r border-[var(--border)] transition-transform duration-200 ease-in-out
          w-60 ${open ? "translate-x-0" : "-translate-x-full"}`}
      >
        {/* Gradient top accent */}
        <div className="h-1 animate-gradient" style={{ background: "var(--gradient-hero)" }} />

        {/* Logo area */}
        <div className="px-5 py-5 border-b border-[var(--border)] flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <Image
              src="/logo.svg"
              alt="Rahul Jindal"
              width={38}
              height={38}
              className="rounded-full"
            />
            <div>
              <div className="text-sm font-bold text-[var(--foreground)] group-hover:text-[var(--cyan-deep)] transition-colors">
                Property Intelligence
              </div>
              <div className="text-[9px] font-bold tracking-[0.18em] text-[var(--dimmed)] uppercase">
                Intelligence Hub
              </div>
            </div>
          </Link>
          <button
            onClick={onToggle}
            className="text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors p-1"
            aria-label="Close sidebar"
          >
            ✕
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => { if (window.innerWidth < 768) onToggle(); }}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all group
                  ${
                    isActive
                      ? "bg-[var(--surface)] shadow-sm font-semibold text-[var(--foreground)]"
                      : "text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--surface)]"
                  }`}
              >
                <span className="text-base">{item.icon}</span>
                <span className="text-xs font-semibold tracking-wide">
                  {item.label}
                </span>
                {isActive && (
                  <span
                    className="ml-auto w-1.5 h-1.5 rounded-full"
                    style={{ background: item.color }}
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Contact footer */}
        <div className="px-5 py-4 border-t border-[var(--border)]">
          <div className="text-[9px] font-bold tracking-[0.18em] text-[var(--dimmed)] uppercase mb-2">
            Contact
          </div>
          <div className="space-y-1.5">
            <a href="mailto:jind3091@mylaurier.ca" className="block text-xs text-[var(--muted)] hover:text-[var(--cyan-deep)] transition-colors">
              jind3091@mylaurier.ca
            </a>
            <a href="https://www.linkedin.com/in/rahuljindal-cs/" target="_blank" className="block text-xs text-[var(--muted)] hover:text-[var(--cyan-deep)] transition-colors">
              LinkedIn
            </a>
            <a href="https://github.com/RahulJindal2006" target="_blank" className="block text-xs text-[var(--muted)] hover:text-[var(--cyan-deep)] transition-colors">
              GitHub
            </a>
          </div>
        </div>
      </aside>
    </>
  );
}
