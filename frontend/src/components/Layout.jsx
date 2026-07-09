import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  Users,
  LogOut,
  Menu,
  X,
  Building2,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Panel principal", icon: LayoutDashboard },
  { to: "/fichas", label: "Fichas de familias", icon: FileText, end: false },
];

const ROLE_LABELS = {
  admin: "Administrador",
  editor: "Editor",
  lector: "Solo lectura",
};

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const items = isAdmin
    ? [...NAV_ITEMS, { to: "/usuarios", label: "Usuarios", icon: Users }]
    : NAV_ITEMS;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="flex h-screen bg-surface">
      {/* Overlay movil */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed z-40 flex h-full w-64 flex-col bg-navy transition-transform duration-200 lg:static lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center gap-2 border-b border-white/10 px-5 py-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-red">
            <Building2 size={20} className="text-white" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-bold text-white">Fichas de Familias</p>
            <p className="text-xs text-white/50">Fase 1 · Estandarización</p>
          </div>
          <button
            className="ml-auto text-white/70 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {items.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-white/10 text-white"
                    : "text-white/70 hover:bg-white/5 hover:text-white"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-white/10 px-3 py-4">
          <div className="mb-2 rounded-lg bg-white/5 px-3 py-2.5">
            <p className="truncate text-sm font-semibold text-white">{user?.nombre}</p>
            <p className="text-xs text-white/50">{ROLE_LABELS[user?.rol] || user?.rol}</p>
          </div>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white/70 transition-colors hover:bg-white/5 hover:text-white"
          >
            <LogOut size={18} />
            Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Contenido principal */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex items-center gap-3 border-b border-surface-border bg-white px-4 py-3 lg:hidden">
          <button onClick={() => setSidebarOpen(true)} className="text-navy">
            <Menu size={22} />
          </button>
          <p className="text-sm font-bold text-navy">Fichas de Familias</p>
        </header>
        <main className="flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
