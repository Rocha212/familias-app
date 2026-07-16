import { useEffect, useState } from "react";
import { Save, Loader2 } from "lucide-react";
import Spinner from "./Spinner";
import MatrizAnios from "./MatrizAnios";
import { Field, TagInput, inputClass } from "./FichaFormFields";
import { getFamilia, createFamilia, updateFamilia } from "../api/familias";
import { extractErrorMessage } from "./FichaFormFields";

const EMPTY_FORM = {
  linea_abastecimiento: "",
  descripcion_familia: "",
  lider: "",
  status: { num_proveedores: 0, num_ocs: 0 },
  analisis_interno: {
    spend: { y_menos_1: 0, y: 0, y_mas_1: 0 },
    pct_cobertura: { y_menos_1: 0, y: 0, y_mas_1: 0 },
    spend_under_control: { y_menos_1: 0, y: 0, y_mas_1: 0 },
  },
  analisis_dofa: { debilidades: "", fortalezas: "", oportunidades: "", amenazas: "" },
  factores_relevantes: { insights: "", indicadores_economicos_financieros: "" },
  clasificacion_proveedores: { apalancados: [], estrategicos: [], rutinarios: [], cuello_de_botella: [] },
  kraljic: "",
  poder_negociacion: { veolia: "", proveedor: "" },
  actores_principales: "",
  premisas_negociacion: "",
  clasificacion_cliente_interno: {
    recurrentes: { spend: 0, ocs: 0 },
    ocasionales: { spend: 0, ocs: 0 },
  },
  subfamilias: "",
  estrategia_aplicar: "",
  estado: "borrador",
};

const ANALISIS_INTERNO_COLUMNS = [
  { key: "y_menos_1", label: "Y-1" },
  { key: "y", label: "Y" },
  { key: "y_mas_1", label: "Y+1" },
];
const ANALISIS_INTERNO_ROWS = [
  { key: "spend", label: "Spend" },
  { key: "pct_cobertura", label: "% Cobertura" },
  { key: "spend_under_control", label: "Spend U. Contr." },
];

export default function FichaFormPagina1({ familiaId, onSaved }) {
  const isEdit = Boolean(familiaId);
  const [form, setForm] = useState(EMPTY_FORM);
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isEdit) return;
    getFamilia(familiaId)
      .then((data) => {
        const { id, created_at, updated_at, created_by_id, creador_nombre, modificador_nombre, ...rest } = data;
        setForm(rest);
      })
      .finally(() => setLoading(false));
  }, [familiaId, isEdit]);

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
    try {
      const payload = {
        ...form,
        kraljic: form.kraljic || null,
        poder_negociacion: {
          veolia: form.poder_negociacion.veolia || null,
          proveedor: form.poder_negociacion.proveedor || null,
        },
      };
      const saved = isEdit ? await updateFamilia(familiaId, payload) : await createFamilia(payload);
      onSaved(saved);
    } catch (err) {
      setError(extractErrorMessage(err, "No fue posible guardar la ficha. Verifica los datos."));
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

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Encabezado</h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Field label="Línea de abastecimiento *">
            <input
              required
              value={form.linea_abastecimiento}
              onChange={(e) => setField("linea_abastecimiento", e.target.value)}
              className={inputClass}
            />
          </Field>
          <Field label="Líder">
            <input value={form.lider} onChange={(e) => setField("lider", e.target.value)} className={inputClass} />
          </Field>
        </div>
        <Field label="Descripción de familia">
          <textarea
            rows={2}
            value={form.descripcion_familia}
            onChange={(e) => setField("descripcion_familia", e.target.value)}
            className={inputClass}
          />
        </Field>
        <Field label="Estado de la ficha">
          <select value={form.estado} onChange={(e) => setField("estado", e.target.value)} className={inputClass}>
            <option value="borrador">Borrador</option>
            <option value="activa">Activa</option>
            <option value="archivada">Archivada</option>
          </select>
        </Field>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Status</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="# Proveedores">
            <input
              type="number"
              value={form.status.num_proveedores}
              onChange={(e) => setField("status.num_proveedores", Number(e.target.value))}
              className={inputClass}
            />
          </Field>
          <Field label="# OCs">
            <input
              type="number"
              value={form.status.num_ocs}
              onChange={(e) => setField("status.num_ocs", Number(e.target.value))}
              className={inputClass}
            />
          </Field>
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Análisis interno (Y-1 / Y / Y+1)
        </h2>
        <MatrizAnios
          columns={ANALISIS_INTERNO_COLUMNS}
          rows={ANALISIS_INTERNO_ROWS}
          value={form.analisis_interno}
          inputType="number"
          onChange={(rowKey, colKey, value) => setField(`analisis_interno.${rowKey}.${colKey}`, value)}
        />
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Clasificación de proveedores (matriz Kraljic)
        </h2>
        <TagInput
          label="Apalancados"
          values={form.clasificacion_proveedores.apalancados}
          onChange={(v) => setField("clasificacion_proveedores.apalancados", v)}
        />
        <TagInput
          label="Estratégicos"
          values={form.clasificacion_proveedores.estrategicos}
          onChange={(v) => setField("clasificacion_proveedores.estrategicos", v)}
        />
        <TagInput
          label="Rutinarios"
          values={form.clasificacion_proveedores.rutinarios}
          onChange={(v) => setField("clasificacion_proveedores.rutinarios", v)}
        />
        <TagInput
          label="Cuello de botella"
          values={form.clasificacion_proveedores.cuello_de_botella}
          onChange={(v) => setField("clasificacion_proveedores.cuello_de_botella", v)}
        />

        <Field label="Cuadrante Kraljic de la familia" hint="Clasificación de la familia según la matriz de Kraljic.">
          <select value={form.kraljic || ""} onChange={(e) => setField("kraljic", e.target.value)} className={inputClass}>
            <option value="">Sin definir</option>
            <option value="estrategico">Estratégico</option>
            <option value="cuello_de_botella">Cuello de botella</option>
            <option value="apalancamiento">Apalancamiento</option>
            <option value="rutinario">Rutinario</option>
          </select>
        </Field>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Análisis DOFA</h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Field label="Debilidades">
            <textarea rows={3} value={form.analisis_dofa.debilidades} onChange={(e) => setField("analisis_dofa.debilidades", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Oportunidades">
            <textarea rows={3} value={form.analisis_dofa.oportunidades} onChange={(e) => setField("analisis_dofa.oportunidades", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Fortalezas">
            <textarea rows={3} value={form.analisis_dofa.fortalezas} onChange={(e) => setField("analisis_dofa.fortalezas", e.target.value)} className={inputClass} />
          </Field>
          <Field label="Amenazas">
            <textarea rows={3} value={form.analisis_dofa.amenazas} onChange={(e) => setField("analisis_dofa.amenazas", e.target.value)} className={inputClass} />
          </Field>
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Factores relevantes</h2>
        <Field label="Insights">
          <textarea rows={3} value={form.factores_relevantes.insights} onChange={(e) => setField("factores_relevantes.insights", e.target.value)} className={inputClass} />
        </Field>
        <Field label="Indicadores económicos y financieros">
          <textarea
            rows={3}
            value={form.factores_relevantes.indicadores_economicos_financieros}
            onChange={(e) => setField("factores_relevantes.indicadores_economicos_financieros", e.target.value)}
            className={inputClass}
          />
        </Field>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
          Actores, poder de negociación y premisas
        </h2>
        <Field label="Actores principales" hint="Principales proveedores y productos que maneja.">
          <textarea rows={3} value={form.actores_principales} onChange={(e) => setField("actores_principales", e.target.value)} className={inputClass} />
        </Field>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Poder de negociación — Veolia">
            <select value={form.poder_negociacion.veolia || ""} onChange={(e) => setField("poder_negociacion.veolia", e.target.value)} className={inputClass}>
              <option value="">Sin definir</option>
              <option value="bajo">Bajo</option>
              <option value="alto">Alto</option>
            </select>
          </Field>
          <Field label="Poder de negociación — Proveedor">
            <select value={form.poder_negociacion.proveedor || ""} onChange={(e) => setField("poder_negociacion.proveedor", e.target.value)} className={inputClass}>
              <option value="">Sin definir</option>
              <option value="bajo">Bajo</option>
              <option value="alto">Alto</option>
            </select>
          </Field>
        </div>
        <Field label="Premisas de negociación">
          <textarea rows={3} value={form.premisas_negociacion} onChange={(e) => setField("premisas_negociacion", e.target.value)} className={inputClass} />
        </Field>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Clasificación cliente interno</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {["recurrentes", "ocasionales"].map((key) => (
            <div key={key} className="rounded-lg border border-surface-border p-3">
              <p className="mb-2 text-xs font-semibold capitalize text-slate-600">{key}</p>
              <Field label="Spend ($)">
                <input
                  type="number"
                  step="any"
                  value={form.clasificacion_cliente_interno[key].spend}
                  onChange={(e) => setField(`clasificacion_cliente_interno.${key}.spend`, Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
              <Field label="# OCs">
                <input
                  type="number"
                  value={form.clasificacion_cliente_interno[key].ocs}
                  onChange={(e) => setField(`clasificacion_cliente_interno.${key}.ocs`, Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
        <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Subfamilias y estrategia</h2>
        <Field label="Subfamilias" hint="Indique las subfamilias asociadas.">
          <textarea rows={2} value={form.subfamilias} onChange={(e) => setField("subfamilias", e.target.value)} className={inputClass} />
        </Field>
        <Field label="Estrategia a aplicar">
          <textarea rows={3} value={form.estrategia_aplicar} onChange={(e) => setField("estrategia_aplicar", e.target.value)} className={inputClass} />
        </Field>
      </section>

      <div className="flex justify-end gap-3 pb-4">
        <button
          type="submit"
          disabled={saving}
          className="flex items-center gap-2 rounded-lg bg-navy px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-light disabled:opacity-60"
        >
          {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
          {isEdit ? "Guardar página 1" : "Crear ficha y continuar"}
        </button>
      </div>
    </form>
  );
}