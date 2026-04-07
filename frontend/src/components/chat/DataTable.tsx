export default function DataTable({
  data,
}: {
  data: Record<string, unknown>[];
}) {
  if (!data || data.length === 0) return null;

  const columns = Object.keys(data[0]);

  return (
    <div className="bg-white border border-[var(--border)] rounded-xl overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--border)] bg-[var(--surface)]">
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-4 py-2.5 text-left text-[11px] font-bold tracking-wider text-[var(--muted)] uppercase whitespace-nowrap"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr
                key={i}
                className="border-b border-[var(--border-light)] hover:bg-[var(--surface)] transition-colors"
              >
                {columns.map((col) => (
                  <td
                    key={col}
                    className="px-4 py-2 text-[13px] text-[var(--foreground)] whitespace-nowrap"
                  >
                    {row[col] != null ? String(row[col]) : "-"}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.length > 10 && (
        <div className="px-4 py-2 text-[11px] text-[var(--muted)] border-t border-[var(--border)]">
          Showing {data.length} rows
        </div>
      )}
    </div>
  );
}
