import { useEffect, useState, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  Plus,
  Search,
  Eye,
  Pencil,
  Trash2,
  Copy,
  Printer,
  Download,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from "lucide-react";
import Layout from "../components/Layout";
import Spinner from "../components/Spinner";
import ConfirmDialog from "../components/ConfirmDialog";
import { useAuth } from "../context/AuthContext";
import { listFamilias, deleteFamilia, duplicateFamilia, downloadFamiliaPdf } from "../api/familias";

const ESTADO_LABELS = { borrador: "Borrador", activa: "Activa", archivada: "Archivada" };
const ESTADO_STYLES = {
  borrador: "bg-slate-100 text-slate-600",
  activa: "bg-green-100 text-green-700",
  archivada: "bg-amber-100 text-amber-700",
};
const KRALJIC_LABELS = {
  estrategico: "Estratégico",
  cuello_de_botella: "Cuello de botella",
  apalancamiento: "Apalancamiento",
  rutinario: "Rutinario",
};

export default function FichasList() {
  const [params, setParams] = useSearchParams();
  const [data, setData] = useState({ items: [], total: 0, page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(true);
  const [searchInput, setSearchInput] = useState(params.get("search") || "");
  const [toDelete, setToDelete] = useState(null);
  const navigate = useNavigate();
  const { isEditor, isAdmin } = useAuth();

  const page = Number(params.get("page") || 1);
  const search = params.get("search") || "";
  const estado = params.get("estado") || "";
  const kraljic = params.get("kraljic") || "";
  const sortBy = params.get("sort_by") || "created_at";
  const sortDir = params.get("sort_dir") || "desc";

  const load = useCallback(() => {
    setLoading(true);
    listFamilias({
      page,
      page_size: 10,
      search: search || undefined,
      estado: estado || undefined,
      kraljic: kraljic || undefined,
      sort_by: sortBy,
      sort_dir: sortDir,
    })
      .then(setData)
      .finally(() => setLoading(false));
  }, [page, search, estado, kraljic, sortBy, sortDir]);

  useEffect(() => {
    load();
  }, [load]);

  const updateParam = (key, value) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    next.set("page", "1");
    setParams(next);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    updateParam("search", searchInput);
  };

  const toggleSort = (column) => {
    const next = new URLSearchParams(params);
    if (sortBy === column) {
      next.set("sort_dir", sortDir === "asc" ? "desc" : "asc");
    } else {
      next.set("sort_by", column);
      next.set("sort_dir", "asc");
    }
    setParams(next);
  };

  const goToPage = (p) => {
    const next = new URLSearchParams(params);
    next.set("page", String(p));
    setParams(next);
  };

  const handleDelete = async () => {
    await deleteFamilia(toDelete.id);
    setToDelete(null);
    load();
  };

  const handleDuplicate = async (id) => {
    const copia = await duplicateFamilia(id);
    navigate(`/fichas/${copia.id}/editar`);
  };

  const SortHeader = ({ column, children }) => (
    <button
      onClick={() => toggleSort(column)}
      className="flex items-center gap-1 text-xs font-semibold uppercase tracking-wide text-slate-500 hover:text-navy"
    >
      {children}
      <ArrowUpDown size={12} className={sortBy === column ? "text-navy" : "text-slate-300"} />
    </button>
  );

  return (
    <Layout>
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-navy">Fichas de familias</h1>
            <p className="text-sm text-slate-500">{data.total} fichas registradas</p>
          </div>
          {isEditor && (
            <button
              onClick={() => navigate("/fichas/nueva")}
              className="flex items-center justify-center gap-2 rounded-lg bg-brand-red px-4 py-2.5 text-sm font-semibold text-white shadow-card hover:bg-brand-redDark"
            >
              <Plus size={18} />
              Nueva ficha
            </button>
          )}
        </div>

        {/* Filtros */}
        <div className="mb-4 flex flex-col gap-3 rounded-xl2 border border-surface-border bg-white p-4 shadow-card sm:flex-row sm:items-center">
          <form onSubmit={handleSearchSubmit} className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder="Buscar ficha..."
              className="w-full rounded-lg border border-surface-border py-2 pl-9 pr-3 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20"
            />
          </form>

          <select
            value={estado}
            onChange={(e) => updateParam("estado", e.target.value)}
            className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
          >
            <option value="">Todos los estados</option>
            <option value="borrador">Borrador</option>
            <option value="activa">Activa</option>
            <option value="archivada">Archivada</option>
          </select>

          <select
            value={kraljic}
            onChange={(e) => updateParam("kraljic", e.target.value)}
            className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
          >
            <option value="">Todos los cuadrantes</option>
            <option value="estrategico">Estratégico</option>
            <option value="cuello_de_botella">Cuello de botella</option>
            <option value="apalancamiento">Apalancamiento</option>
            <option value="rutinario">Rutinario</option>
          </select>
        </div>

        {/* Tabla */}
        <div className="overflow-hidden rounded-xl2 border border-surface-border bg-white shadow-card">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-surface">
                <tr>
                  <th className="px-4 py-3 text-left">
                    <SortHeader column="linea_abastecimiento">Línea de abastecimiento</SortHeader>
                  </th>
                  <th className="px-4 py-3 text-left">
                    <SortHeader column="lider">Líder</SortHeader>
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Kraljic
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Estado
                  </th>
                  <th className="px-4 py-3 text-left">
                    <SortHeader column="updated_at">Última modificación</SortHeader>
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border">
                {loading && (
                  <tr>
                    <td colSpan={6} className="py-12 text-center">
                      <Spinner />
                    </td>
                  </tr>
                )}
                {!loading && data.items.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-400">
                      No se encontraron fichas con los filtros actuales.
                    </td>
                  </tr>
                )}
                {!loading &&
                  data.items.map((f) => (
                    <tr key={f.id} className="hover:bg-surface">
                      <td className="px-4 py-3 font-medium text-slate-800">{f.linea_abastecimiento}</td>
                      <td className="px-4 py-3 text-slate-600">{f.lider || "—"}</td>
                      <td className="px-4 py-3 text-slate-600">
                        {f.kraljic ? KRALJIC_LABELS[f.kraljic] : "—"}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`rounded-full px-2.5 py-1 text-xs font-semibold ${ESTADO_STYLES[f.estado]}`}
                        >
                          {ESTADO_LABELS[f.estado]}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-500">
                        {new Date(f.updated_at).toLocaleDateString("es-CO", {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                        })}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            title="Ver"
                            onClick={() => navigate(`/fichas/${f.id}`)}
                            className="rounded-md p-1.5 text-slate-500 hover:bg-navy/10 hover:text-navy"
                          >
                            <Eye size={16} />
                          </button>
                          {isEditor && (
                            <button
                              title="Editar"
                              onClick={() => navigate(`/fichas/${f.id}/editar`)}
                              className="rounded-md p-1.5 text-slate-500 hover:bg-navy/10 hover:text-navy"
                            >
                              <Pencil size={16} />
                            </button>
                          )}
                          <button
                            title="Descargar PDF"
                            onClick={() => downloadFamiliaPdf(f.id, `ficha_${f.id}.pdf`)}
                            className="rounded-md p-1.5 text-slate-500 hover:bg-navy/10 hover:text-navy"
                          >
                            <Download size={16} />
                          </button>
                          {isEditor && (
                            <button
                              title="Duplicar"
                              onClick={() => handleDuplicate(f.id)}
                              className="rounded-md p-1.5 text-slate-500 hover:bg-navy/10 hover:text-navy"
                            >
                              <Copy size={16} />
                            </button>
                          )}
                          {isAdmin && (
                            <button
                              title="Eliminar"
                              onClick={() => setToDelete(f)}
                              className="rounded-md p-1.5 text-slate-500 hover:bg-brand-red/10 hover:text-brand-red"
                            >
                              <Trash2 size={16} />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>

          {/* Paginacion */}
          <div className="flex items-center justify-between border-t border-surface-border px-4 py-3">
            <p className="text-xs text-slate-500">
              Página {data.page} de {data.total_pages}
            </p>
            <div className="flex gap-2">
              <button
                disabled={page <= 1}
                onClick={() => goToPage(page - 1)}
                className="rounded-md border border-surface-border p-1.5 text-slate-500 disabled:opacity-40"
              >
                <ChevronLeft size={16} />
              </button>
              <button
                disabled={page >= data.total_pages}
                onClick={() => goToPage(page + 1)}
                className="rounded-md border border-surface-border p-1.5 text-slate-500 disabled:opacity-40"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>

      <ConfirmDialog
        open={!!toDelete}
        title="Eliminar ficha"
        message={`¿Deseas eliminar la ficha "${toDelete?.linea_abastecimiento}"? Esta acción no se puede deshacer.`}
        onConfirm={handleDelete}
        onCancel={() => setToDelete(null)}
      />
    </Layout>
  );
}
