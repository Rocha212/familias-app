import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Pencil, Printer, Download, Copy } from "lucide-react";
import Layout from "../components/Layout";
import Spinner from "../components/Spinner";
import FichaPreview from "../components/FichaPreview";
import { useAuth } from "../context/AuthContext";
import { getFamilia, downloadFamiliaPdf, duplicateFamilia } from "../api/familias";

export default function FichaView() {
  const { id } = useParams();
  const [ficha, setFicha] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { isEditor } = useAuth();

  useEffect(() => {
    setLoading(true);
    getFamilia(id)
      .then(setFicha)
      .finally(() => setLoading(false));
  }, [id]);

  const handleDuplicate = async () => {
    const copia = await duplicateFamilia(id);
    navigate(`/fichas/${copia.id}/editar`);
  };

  return (
    <Layout>
      <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3 print:hidden">
          <button
            onClick={() => navigate("/fichas")}
            className="flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-navy"
          >
            <ArrowLeft size={16} />
            Volver al listado
          </button>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => window.print()}
              className="flex items-center gap-2 rounded-lg border border-surface-border bg-white px-3.5 py-2 text-sm font-medium text-slate-600 hover:bg-surface"
            >
              <Printer size={16} />
              Imprimir
            </button>
            <button
              onClick={() => ficha && downloadFamiliaPdf(ficha.id, `ficha_${ficha.id}.pdf`)}
              className="flex items-center gap-2 rounded-lg border border-surface-border bg-white px-3.5 py-2 text-sm font-medium text-slate-600 hover:bg-surface"
            >
              <Download size={16} />
              Exportar PDF
            </button>
            {isEditor && (
              <>
                <button
                  onClick={handleDuplicate}
                  className="flex items-center gap-2 rounded-lg border border-surface-border bg-white px-3.5 py-2 text-sm font-medium text-slate-600 hover:bg-surface"
                >
                  <Copy size={16} />
                  Duplicar
                </button>
                <button
                  onClick={() => navigate(`/fichas/${id}/editar`)}
                  className="flex items-center gap-2 rounded-lg bg-navy px-3.5 py-2 text-sm font-semibold text-white hover:bg-navy-light"
                >
                  <Pencil size={16} />
                  Editar
                </button>
              </>
            )}
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner />
          </div>
        ) : (
          <FichaPreview ficha={ficha} />
        )}
      </div>
    </Layout>
  );
}
