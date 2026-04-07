"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();
  const isLanding = pathname === "/";

  return (
    <>
      <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <main
        className="flex-1 min-h-screen transition-all duration-200 ease-in-out"
        style={{
          marginLeft: !isLanding && sidebarOpen ? "15rem" : "0",
        }}
      >
        {children}
      </main>
    </>
  );
}
