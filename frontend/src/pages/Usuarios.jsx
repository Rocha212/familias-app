import { useEffect, useState } from "react";
import { Plus, X, Loader2 } from "lucide-react";
import Layout from "../components/Layout";
import Spinner from "../components/Spinner";
import { listUsuarios, createUsuario, updateUsuario } from "../api/users";

const ROLE_LABELS = { admin: "Administrador", editor: "Editor", lector: "Solo lectura" };

const EMPTY_USER = { email: "", nombre: "", rol: "lector", password: "" };

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_USER);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    listUsuarios()
      .then(setUsuarios)
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await createUsuario(form);
      setForm(EMPTY_USER);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "No fue posible crear el usuario.");
    } finally {
      setSaving(false);
    }
  };

  const toggleActive = async (user) => {
    await updateUsuario(user.id, { is_active: !user.is_active });
    load();
  };

  return (
    <Layout>
      <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-navy">Usuarios</h1>
            <p className="text-sm text-slate-500">Gestión de accesos y roles del sistema.</p>
          </div>
          <button
            onClick={() => setShowForm((s) => !s)}
            className="flex items-center gap-2 rounded-lg bg-brand-red px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-redDark"
          >
            {showForm ? <X size={18} /> : <Plus size={18} />}
            {showForm ? "Cancelar" : "Nuevo usuario"}
          </button>
        </div>

        {showForm && (
          <form
            onSubmit={handleCreate}
            className="mb-6 rounded-xl2 border border-surface-border bg-white p-5 shadow-card"
          >
            {error && (
              <div className="mb-4 rounded-lg bg-brand-red/10 px-3 py-2 text-sm text-brand-red">{error}</div>
            )}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <input
                required
                placeholder="Nombre completo"
                value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
              />
              <input
                required
                type="email"
                placeholder="Correo institucional"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
              />
              <select
                value={form.rol}
                onChange={(e) => setForm({ ...form, rol: e.target.value })}
                className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
              >
                <option value="lector">Solo lectura</option>
                <option value="editor">Editor</option>
                <option value="admin">Administrador</option>
              </select>
              <input
                required
                type="password"
                placeholder="Contraseña temporal"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy"
              />
            </div>
            <button
              type="submit"
              disabled={saving}
              className="mt-4 flex items-center gap-2 rounded-lg bg-navy px-4 py-2 text-sm font-semibold text-white hover:bg-navy-light disabled:opacity-60"
            >
              {saving && <Loader2 size={16} className="animate-spin" />}
              Crear usuario
            </button>
          </form>
        )}

        <div className="overflow-hidden rounded-xl2 border border-surface-border bg-white shadow-card">
          {loading ? (
            <div className="flex justify-center py-16">
              <Spinner />
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-surface">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">
                    Nombre
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">
                    Correo
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">
                    Rol
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">
                    Estado
                  </th>
                  <th className="px-4 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border">
                {usuarios.map((u) => (
                  <tr key={u.id}>
                    <td className="px-4 py-3 font-medium text-slate-800">{u.nombre}</td>
                    <td className="px-4 py-3 text-slate-600">{u.email}</td>
                    <td className="px-4 py-3 text-slate-600">{ROLE_LABELS[u.rol]}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
                          u.is_active ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {u.is_active ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => toggleActive(u)}
                        className="text-xs font-semibold text-navy hover:underline"
                      >
                        {u.is_active ? "Desactivar" : "Activar"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </Layout>
  );
}
