import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import FichasList from "./pages/FichasList";
import FichaView from "./pages/FichaView";
import FichaForm from "./pages/FichaForm";
import Usuarios from "./pages/Usuarios";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<Login />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/fichas"
        element={
          <ProtectedRoute>
            <FichasList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/fichas/nueva"
        element={
          <ProtectedRoute>
            <FichaForm />
          </ProtectedRoute>
        }
      />
      <Route
        path="/fichas/:id"
        element={
          <ProtectedRoute>
            <FichaView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/fichas/:id/editar"
        element={
          <ProtectedRoute>
            <FichaForm />
          </ProtectedRoute>
        }
      />

      <Route
        path="/usuarios"
        element={
          <ProtectedRoute adminOnly>
            <Usuarios />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
