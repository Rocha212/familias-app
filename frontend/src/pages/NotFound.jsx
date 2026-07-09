import { useNavigate } from "react-router-dom";

export default function NotFound() {
  const navigate = useNavigate();
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-surface text-center">
      <p className="text-6xl font-extrabold text-navy">404</p>
      <p className="mt-2 text-slate-500">La página que buscas no existe.</p>
      <button
        onClick={() => navigate("/dashboard")}
        className="mt-6 rounded-lg bg-navy px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-light"
      >
        Volver al panel principal
      </button>
    </div>
  );
}
