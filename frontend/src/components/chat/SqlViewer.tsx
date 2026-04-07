"use client";

import { useState } from "react";

export default function SqlViewer({ sql }: { sql: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl overflow-hidden shadow-sm">
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700">
        <span className="text-[10px] font-bold tracking-widest text-slate-400 uppercase">
          SQL Query
        </span>
        <button
          onClick={handleCopy}
          className="text-[11px] font-semibold text-cyan-400 hover:text-white transition-colors"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <pre className="px-4 py-3 text-[13px] text-cyan-300 overflow-x-auto font-mono whitespace-pre-wrap">
        {sql}
      </pre>
    </div>
  );
}
