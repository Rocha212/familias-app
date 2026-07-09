import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Building2, Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/dashboard";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(
        err.response?.data?.detail || "No fue posible iniciar sesión. Verifica tus datos."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-navy px-4">
      <div className="w-full max-w-md">
        <div className="mb-6 flex flex-col items-center text-white">
          <div className="mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-red">
            <Building2 size={28} />
          </div>
          <h1 className="text-xl font-bold">Gestión de Fichas de Estandarización</h1>
          <p className="mt-1 text-sm text-white/60">Familias de abastecimiento · Fase 1</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-xl2 bg-white p-7 shadow-panel"
        >
          <h2 className="mb-5 text-lg font-bold text-navy">Iniciar sesión</h2>

          {error && (
            <div className="mb-4 rounded-lg bg-brand-red/10 px-3 py-2 text-sm text-brand-red">
              {error}
            </div>
          )}

          <label className="mb-1 block text-sm font-medium text-slate-600">
            Correo institucional
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="usuario@empresa.com"
            className="mb-4 w-full rounded-lg border border-surface-border px-3 py-2.5 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20"
          />

          <label className="mb-1 block text-sm font-medium text-slate-600">Contraseña</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="mb-6 w-full rounded-lg border border-surface-border px-3 py-2.5 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20"
          />

          <button
            type="submit"
            disabled={loading}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-navy py-2.5 text-sm font-semibold text-white transition-colors hover:bg-navy-light disabled:opacity-60"
          >
            {loading && <Loader2 size={16} className="animate-spin" />}
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
}
