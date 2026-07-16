import { useEffect, useState } from "react";
import { Save, Loader2 } from "lucide-react";
import Spinner from "./Spinner";
import MatrizAnios from "./MatrizAnios";
import { getRevisionEstrategica, updateRevisionEstrategica } from "../api/revisiones";
import { extractErrorMessage } from "./FichaFormFields";

const ANIOS_COLUMNS = [
  { key: "2026", label: "2026" },
  { key: "2027", label: "2027" },
  { key: "2028", label: "2028" },
];

const EJES_ROWS = [
  { key: "spend_under_control", label: "Spend Under Control" },
  { key: "performance_economico", label: "Performance Económico" },
  { key: "performance_operativo", label: "Performance Operativo" },
  { key: "riesgo", label: "Riesgo" },
  { key: "innovacion", label: "Innovación" },
  { key: "crecimiento_ingresos", label: "Crecimiento Ingresos" },
  { key: "ambiental_social_gobernanza", label: "Ambiental-Social-Gobernanza" },
];

const EMPTY_BENEFICIOS = Object.fromEntries(
  EJES_ROWS.map((row) => [row.key, { "2026": "", "2027": "", "2028": "" }])
);

export default function FichaFormPagina3({ familiaId }) {
  const [beneficios, setBeneficios] = useState(EMPTY_BENEFICIOS);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getRevisionEstrategica(familiaId)
      .then((data) => setBeneficios(data.beneficios_esperados))
      .finally(() => setLoading(false));
  }, [familiaId]);

  const handleChange = (rowKey, colKey, value) => {
    setBeneficios((prev) => ({ ...prev, [rowKey]: { ...prev[rowKey], [colKey]: value } }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setSaved(false);
    try {
      await updateRevisionEstrategica(familiaId, { beneficios_esperados: beneficios });
      setSaved(true);
    } catch (err) {
      setError(extractErrorMessage(err, "No fue posible guardar esta página."));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Spinner />
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <div className="rounded-lg bg-brand-red/10 px-4 py-3 text-sm text-brand-red">{error}</div>}
      {saved && (
        <div className="rounded-lg bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
          Página 3 guardada correctamente.
        </div>
      )}

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Beneficios esperados a 3 años
        </h2>
        <MatrizAnios columns={ANIOS_COLUMNS} rows={EJES_ROWS} value={beneficios} inputType="text" onChange={handleChange} />
      </section>

      <div className="flex justify-end gap-3 pb-4">
        <button
          type="submit"
          disabled={saving}
          className="flex items-center gap-2 rounded-lg bg-navy px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-light disabled:opacity-60"
        >
          {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
          Guardar página 3
        </button>
      </div>
    </form>
  );
}