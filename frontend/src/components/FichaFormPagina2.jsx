import { useEffect, useState } from "react";
import { Save, Loader2 } from "lucide-react";
import Spinner from "./Spinner";
import { Field, inputClass } from "./FichaFormFields";
import { getRevisionEstrategica, updateRevisionEstrategica } from "../api/revisiones";
import { extractErrorMessage } from "./FichaFormFields";

const EMPTY_REVISION_P2 = {
  objetivo_estrategico: "",
  ejes_estrategicos: {
    performance_economico: "",
    performance_operacional: "",
    riesgo: { compliance: "", financiero: "", operativo: "", ambiental_pss: "" },
    innovacion: { general: "", crecimiento_ingresos: "" },
    ambiental_social_gobernanza: {
      decarbonizacion: "",
      economia_circular: "",
      creacion_valor_territorial: "",
      derechos_humanos_compliance: "",
    },
  },
  roadmap: { "2026": "", "2027": "", "2028": "" },
};

export default function FichaFormPagina2({ familiaId }) {
  const [form, setForm] = useState(EMPTY_REVISION_P2);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getRevisionEstrategica(familiaId)
      .then((data) => {
        const { objetivo_estrategico, ejes_estrategicos, roadmap } = data;
        setForm({ objetivo_estrategico, ejes_estrategicos, roadmap });
      })
      .finally(() => setLoading(false));
  }, [familiaId]);

  const setField = (path, value) => {
    setForm((prev) => {
      const next = structuredClone(prev);
      const keys = path.split(".");
      let obj = next;
      for (let i = 0; i < keys.length - 1; i++) obj = obj[keys[i]];
      obj[keys[keys.length - 1]] = value;
      return next;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setSaved(false);
    try {
      await updateRevisionEstrategica(familiaId, form);
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

  const { riesgo, innovacion, ambiental_social_gobernanza: asg } = form.ejes_estrategicos;

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <div className="rounded-lg bg-brand-red/10 px-4 py-3 text-sm text-brand-red">{error}</div>}
      {saved && (
        <div className="rounded-lg bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
          Página 2 guardada correctamente.
        </div>
      )}

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Objetivo estratégico de la revisión
        </h2>
        <textarea
          rows={3}
          value={form.objetivo_estrategico}
          onChange={(e) => setField("objetivo_estrategico", e.target.value)}
          className={inputClass}
        />
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Performance</h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Field label="Performance Económico">
            <textarea rows={3} value={form.ejes_estrategicos.performance_economico} onChange={(e) => setField("ejes_estrategicos.performance_economico", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Performance Operacional">
            <textarea rows={3} value={form.ejes_estrategicos.performance_operacional} onChange={(e) => setField("ejes_estrategicos.performance_operacional", e.target.value)} className={inputClass} />
          </Field>
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Riesgo</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Compliance">
            <textarea rows={2} value={riesgo.compliance} onChange={(e) => setField("ejes_estrategicos.riesgo.compliance", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Financiero">
            <textarea rows={2} value={riesgo.financiero} onChange={(e) => setField("ejes_estrategicos.riesgo.financiero", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Operativo">
            <textarea rows={2} value={riesgo.operativo} onChange={(e) => setField("ejes_estrategicos.riesgo.operativo", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Ambiental y PSS">
            <textarea rows={2} value={riesgo.ambiental_pss} onChange={(e) => setField("ejes_estrategicos.riesgo.ambiental_pss", e.target.value)} className={inputClass} />
          </Field>
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Innovación</h2>
        <Field label="Innovación (general)">
          <textarea rows={2} value={innovacion.general} onChange={(e) => setField("ejes_estrategicos.innovacion.general", e.target.value)} className={inputClass} />
        </Field>
        <Field label="Crecimiento Ingresos">
          <textarea rows={2} value={innovacion.crecimiento_ingresos} onChange={(e) => setField("ejes_estrategicos.innovacion.crecimiento_ingresos", e.target.value)} className={inputClass} />
        </Field>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Ambiental - Social - Gobernanza
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Decarbonización">
            <textarea rows={2} value={asg.decarbonizacion} onChange={(e) => setField("ejes_estrategicos.ambiental_social_gobernanza.decarbonizacion", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Economía Circular">
            <textarea rows={2} value={asg.economia_circular} onChange={(e) => setField("ejes_estrategicos.ambiental_social_gobernanza.economia_circular", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Creación de Valor Territorial">
            <textarea rows={2} value={asg.creacion_valor_territorial} onChange={(e) => setField("ejes_estrategicos.ambiental_social_gobernanza.creacion_valor_territorial", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Derechos Humanos y Compliance">
            <textarea rows={2} value={asg.derechos_humanos_compliance} onChange={(e) => setField("ejes_estrategicos.ambiental_social_gobernanza.derechos_humanos_compliance", e.target.value)} className={inputClass} />
          </Field>
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">RoadMap a 3 años</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {["2026", "2027", "2028"].map((anio) => (
            <Field key={anio} label={anio}>
              <textarea rows={4} value={form.roadmap[anio]} onChange={(e) => setField(`roadmap.${anio}`, e.target.value)} className={inputClass} />
            </Field>
          ))}
        </div>
      </section>

      <div className="flex justify-end gap-3 pb-4">
        <button
          type="submit"
          disabled={saving}
          className="flex items-center gap-2 rounded-lg bg-navy px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-light disabled:opacity-60"
        >
          {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
          Guardar página 2
        </button>
      </div>
    </form>
  );
}