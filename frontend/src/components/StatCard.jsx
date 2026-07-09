export default function StatCard({ label, value, icon: Icon, accent = "navy" }) {
  const accentClasses = {
    navy: "bg-navy/10 text-navy",
    red: "bg-brand-red/10 text-brand-red",
    gray: "bg-surface-border/40 text-slate-600",
  };

  return (
    <div className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-1 text-3xl font-bold text-navy">{value}</p>
        </div>
        {Icon && (
          <div className={`flex h-11 w-11 items-center justify-center rounded-full ${accentClasses[accent]}`}>
            <Icon size={22} />
          </div>
        )}
      </div>
    </div>
  );
}
