import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import Layout from "../components/Layout";
import FichaFormPagina1 from "../components/FichaFormPagina1";
import FichaFormPagina2 from "../components/FichaFormPagina2";
import FichaFormPagina3 from "../components/FichaFormPagina3";

const TABS = [
  { key: "pagina1", label: "1. Dónde estamos" },
  { key: "pagina2", label: "2. Dónde queremos llegar" },
  { key: "pagina3", label: "3. Qué resultados esperamos" },
];

export default function FichaForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [familiaId, setFamiliaId] = useState(id ? Number(id) : null);
  const [activeTab, setActiveTab] = useState("pagina1");

  const handlePagina1Saved = (savedFamilia) => {
    const isNew = !familiaId;
    setFamiliaId(savedFamilia.id);
    if (isNew) {
      navigate(`/fichas/${savedFamilia.id}/editar`, { replace: true });
      setActiveTab("pagina2");
    }
  };

  return (
    <Layout>
      <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
        <button
          onClick={() => navigate(-1)}
          className="mb-5 flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-navy"
        >
          <ArrowLeft size={16} />
          Volver
        </button>

        <h1 className="mb-6 text-2xl font-bold text-navy">
          {familiaId ? "Editar ficha" : "Nueva ficha de familia"}
        </h1>

        <div className="mb-6 flex flex-wrap gap-2 border-b border-surface-border">
          {TABS.map((tab) => {
            const disabled = tab.key !== "pagina1" && !familiaId;
            const active = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                type="button"
                disabled={disabled}
                onClick={() => setActiveTab(tab.key)}
                className={`rounded-t-lg px-4 py-2.5 text-sm font-semibold transition ${
                  active
                    ? "border-b-2 border-brand-red text-brand-red"
                    : disabled
                    ? "cursor-not-allowed text-slate-300"
                    : "text-slate-500 hover:text-navy"
                }`}
                title={disabled ? "Primero guarda la página 1 para habilitar esta página" : undefined}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {activeTab === "pagina1" && <FichaFormPagina1 familiaId={familiaId} onSaved={handlePagina1Saved} />}
        {activeTab === "pagina2" && familiaId && <FichaFormPagina2 familiaId={familiaId} />}
        {activeTab === "pagina3" && familiaId && <FichaFormPagina3 familiaId={familiaId} />}
      </div>
    </Layout>
  );
}