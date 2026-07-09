export default function ConfirmDialog({ open, title, message, onConfirm, onCancel, danger = true }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-sm rounded-xl2 bg-white p-6 shadow-panel">
        <h3 className="text-lg font-bold text-navy">{title}</h3>
        <p className="mt-2 text-sm text-slate-600">{message}</p>
        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="rounded-lg border border-surface-border px-4 py-2 text-sm font-medium text-slate-600 hover:bg-surface"
          >
            Cancelar
          </button>
          <button
            onClick={onConfirm}
            className={`rounded-lg px-4 py-2 text-sm font-semibold text-white ${
              danger ? "bg-brand-red hover:bg-brand-redDark" : "bg-navy hover:bg-navy-light"
            }`}
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>
  );
}
