import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  CheckCircle2,
  FileEdit,
  Archive,
  Plus,
  Search,
  ArrowRight,
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import Spinner from "../components/Spinner";
import { fetchDashboard } from "../api/dashboard";

const PIE_COLORS = ["#0B2A5B", "#E2231A", "#4B7BD6", "#F2A65A"];

const ESTADO_LABELS = { borrador: "Borrador", activa: "Activa", archivada: "Archivada" };

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    navigate(`/fichas?search=${encodeURIComponent(search)}`);
  };

  return (
    <Layout>
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-navy">Panel principal</h1>
            <p className="text-sm text-slate-500">
              Resumen general de las fichas de estandarización de familias.
            </p>
          </div>
          <button
            onClick={() => navigate("/fichas/nueva")}
            className="flex items-center justify-center gap-2 rounded-lg bg-brand-red px-4 py-2.5 text-sm font-semibold text-white shadow-card transition-colors hover:bg-brand-redDark"
          >
            <Plus size={18} />
            Nueva ficha
          </button>
        </div>

        <form onSubmit={handleSearch} className="mb-6">
          <div className="relative max-w-lg">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar por línea de abastecimiento, líder o descripción..."
              className="w-full rounded-lg border border-surface-border bg-white py-2.5 pl-10 pr-4 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20"
            />
          </div>
        </form>

        {loading || !data ? (
          <div className="flex justify-center py-20">
            <Spinner />
          </div>
        ) : (
          <>
            <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatCard label="Total de fichas" value={data.total_fichas} icon={FileText} accent="navy" />
              <StatCard label="Fichas activas" value={data.fichas_activas} icon={CheckCircle2} accent="red" />
              <StatCard label="En borrador" value={data.fichas_borrador} icon={FileEdit} accent="gray" />
              <StatCard label="Archivadas" value={data.fichas_archivadas} icon={Archive} accent="gray" />
            </div>

            <div className="mb-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
                <h3 className="mb-4 text-sm font-bold text-navy">Distribución por cuadrante Kraljic</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={data.distribucion_kraljic}
                      dataKey="total"
                      nameKey="categoria"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={2}
                    >
                      {data.distribucion_kraljic.map((_, idx) => (
                        <Cell key={idx} fill={PIE_COLORS[idx % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
                <h3 className="mb-4 text-sm font-bold text-navy">Fichas por estado</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={data.distribucion_estado}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#EAECEF" />
                    <XAxis
                      dataKey="categoria"
                      tickFormatter={(v) => ESTADO_LABELS[v] || v}
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="total" fill="#0B2A5B" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="rounded-xl2 border border-surface-border bg-white shadow-card">
              <div className="flex items-center justify-between border-b border-surface-border px-5 py-4">
                <h3 className="text-sm font-bold text-navy">Últimas fichas creadas</h3>
                <button
                  onClick={() => navigate("/fichas")}
                  className="flex items-center gap-1 text-sm font-medium text-brand-red hover:underline"
                >
                  Ver todas <ArrowRight size={14} />
                </button>
              </div>
              <ul className="divide-y divide-surface-border">
                {data.ultimas_fichas.length === 0 && (
                  <li className="px-5 py-6 text-sm text-slate-400">Aún no hay fichas registradas.</li>
                )}
                {data.ultimas_fichas.map((f) => (
                  <li
                    key={f.id}
                    onClick={() => navigate(`/fichas/${f.id}`)}
                    className="flex cursor-pointer items-center justify-between px-5 py-3.5 hover:bg-surface"
                  >
                    <div>
                      <p className="text-sm font-semibold text-slate-800">{f.linea_abastecimiento}</p>
                      <p className="text-xs text-slate-500">Líder: {f.lider || "—"}</p>
                    </div>
                    <span className="rounded-full bg-navy/5 px-3 py-1 text-xs font-semibold text-navy">
                      {ESTADO_LABELS[f.estado] || f.estado}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}
