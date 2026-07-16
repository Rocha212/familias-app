export default function MatrizAnios({ columns, rows, value, onChange, inputType = "text" }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="w-40 border border-surface-border bg-surface px-2 py-1.5 text-left text-xs font-semibold text-slate-500">
              {" "}
            </th>
            {columns.map((col) => (
              <th
                key={col.key}
                className="border border-surface-border bg-surface px-2 py-1.5 text-center text-xs font-semibold text-slate-500"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.key}>
              <td className="border border-surface-border px-2 py-1.5 text-xs font-medium text-slate-700">
                {row.label}
              </td>
              {columns.map((col) => (
                <td key={col.key} className="border border-surface-border p-1">
                  {inputType === "text" ? (
                    <textarea
                      rows={2}
                      value={value?.[row.key]?.[col.key] ?? ""}
                      onChange={(e) => onChange(row.key, col.key, e.target.value)}
                      className="w-full resize-none rounded border-0 px-1.5 py-1 text-xs outline-none focus:ring-1 focus:ring-navy/30"
                    />
                  ) : (
                    <input
                      type="number"
                      step="any"
                      value={value?.[row.key]?.[col.key] ?? 0}
                      onChange={(e) => onChange(row.key, col.key, Number(e.target.value))}
                      className="w-full rounded border-0 px-1.5 py-1 text-xs outline-none focus:ring-1 focus:ring-navy/30"
                    />
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}