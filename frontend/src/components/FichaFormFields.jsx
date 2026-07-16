import { useState } from "react";
import { X } from "lucide-react";

export const inputClass =
  "w-full rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20";

export function Field({ label, children, hint }) {
  return (
    <div className="mb-4">
      <label className="mb-1 block text-sm font-medium text-slate-600">{label}</label>
      {children}
      {hint && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
    </div>
  );
}

export function TagInput({ label, values, onChange }) {
  const [draft, setDraft] = useState("");

  const addTag = () => {
    const trimmed = draft.trim();
    if (trimmed && !values.includes(trimmed)) {
      onChange([...values, trimmed]);
    }
    setDraft("");
  };

  return (
    <div className="mb-3">
      <p className="mb-1 text-xs font-semibold uppercase text-slate-500">{label}</p>
      <div className="mb-1.5 flex flex-wrap gap-1.5">
        {values.map((v, idx) => (
          <span
            key={idx}
            className="flex items-center gap-1 rounded-full bg-navy/5 px-2.5 py-1 text-xs font-medium text-navy"
          >
            {v}
            <button
              type="button"
              onClick={() => onChange(values.filter((_, i) => i !== idx))}
              className="text-navy/50 hover:text-brand-red"
            >
              <X size={12} />
            </button>
          </span>
        ))}
      </div>
      <input
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            addTag();
          }
        }}
        onBlur={addTag}
        placeholder="Escribe y presiona Enter..."
        className={inputClass}
      />
    </div>
  );
}
export function extractErrorMessage(err, fallback) {
  const detail = err?.response?.data?.detail;
  if (!detail) return fallback;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => (typeof d === "string" ? d : d.msg ? `${(d.loc || []).join(".")}: ${d.msg}` : JSON.stringify(d)))
      .join(" · ");
  }
  return fallback;
}