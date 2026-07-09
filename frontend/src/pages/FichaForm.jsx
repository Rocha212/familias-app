import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Save, X, Loader2 } from "lucide-react";
import Layout from "../components/Layout";
import Spinner from "../components/Spinner";
import { getFamilia, createFamilia, updateFamilia } from "../api/familias";

const EMPTY_FORM = {
  linea_abastecimiento: "",
  descripcion_familia: "",
  lider: "",
  status: { spend_2025: 0, num_proveedores: 0, spend_under_control: 0, num_proveedores_suc: 0 },
  analisis_dofa: "",
  factores_relevantes: "",
  clasificacion_proveedores: { estrategicos: [], clave: [], tacticos: [] },
  kraljic: "",
  actores_principales: "",
  premisas_negociacion: "",
  clasificacion_cliente_interno: {
    estrategicos: { spend: 0, ocs: 0 },
    clave: { spend: 0, ocs: 0 },
    tacticos: { spend: 0, ocs: 0 },
  },
  subfamilias: "",
  estrategia_aplicar: "",
  estado: "borrador",
};

function Field({ label, children, hint }) {
  return (
    <div className="mb-4">
      <label className="mb-1 block text-sm font-medium text-slate-600">{label}</label>
      {children}
      {hint && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
    </div>
  );
}

const inputClass =
  "w-full rounded-lg border border-surface-border px-3 py-2 text-sm outline-none focus:border-navy focus:ring-2 focus:ring-navy/20";

function TagInput({ label, values, onChange }) {
  const [draft, setDraft] = useState("");

  const addTag = () => {
    const trimmed = draft.trim();
    if (trimmed && !values.includes(trimmed)) {
      onChange([...values, trimmed]);
    }
    setDraft("");
  };

  return (
    <div className="mb-3">
      <p className="mb-1 text-xs font-semibold uppercase text-slate-500">{label}</p>
      <div className="mb-1.5 flex flex-wrap gap-1.5">
        {values.map((v, idx) => (
          <span
            key={idx}
            className="flex items-center gap-1 rounded-full bg-navy/5 px-2.5 py-1 text-xs font-medium text-navy"
          >
            {v}
            <button
              type="button"
              onClick={() => onChange(values.filter((_, i) => i !== idx))}
              className="text-navy/50 hover:text-brand-red"
            >
              <X size={12} />
            </button>
          </span>
        ))}
      </div>
      <input
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            addTag();
          }
        }}
        onBlur={addTag}
        placeholder="Escribe y presiona Enter..."
        className={inputClass}
      />
    </div>
  );
}

export default function FichaForm() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const [form, setForm] = useState(EMPTY_FORM);
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!isEdit) return;
    getFamilia(id)
      .then((data) => {
        const { id: _id, created_at, updated_at, created_by_id, creador_nombre, modificador_nombre, ...rest } = data;
        setForm(rest);
      })
      .finally(() => setLoading(false));
  }, [id, isEdit]);

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
      const payload = { ...form, kraljic: form.kraljic || null };
      if (isEdit) {
        await updateFamilia(id, payload);
        navigate(`/fichas/${id}`);
      } else {
        const created = await createFamilia(payload);
        navigate(`/fichas/${created.id}`);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "No fue posible guardar la ficha. Verifica los datos.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <Spinner />
        </div>
      </Layout>
    );
  }

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
          {isEdit ? "Editar ficha" : "Nueva ficha de familia"}
        </h1>

        {error && (
          <div className="mb-5 rounded-lg bg-brand-red/10 px-4 py-3 text-sm text-brand-red">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Encabezado */}
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
                <input
                  value={form.lider}
                  onChange={(e) => setField("lider", e.target.value)}
                  className={inputClass}
                />
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
              <select
                value={form.estado}
                onChange={(e) => setField("estado", e.target.value)}
                className={inputClass}
              >
                <option value="borrador">Borrador</option>
                <option value="activa">Activa</option>
                <option value="archivada">Archivada</option>
              </select>
            </Field>
          </section>

          {/* Status */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">Status</h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <Field label="Spend 2025 ($)">
                <input
                  type="number"
                  step="any"
                  value={form.status.spend_2025}
                  onChange={(e) => setField("status.spend_2025", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
              <Field label="# Proveedores">
                <input
                  type="number"
                  value={form.status.num_proveedores}
                  onChange={(e) => setField("status.num_proveedores", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
              <Field label="Spend bajo control ($)">
                <input
                  type="number"
                  step="any"
                  value={form.status.spend_under_control}
                  onChange={(e) => setField("status.spend_under_control", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
              <Field label="# Proveedores SUC">
                <input
                  type="number"
                  value={form.status.num_proveedores_suc}
                  onChange={(e) => setField("status.num_proveedores_suc", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>
            </div>
          </section>

          {/* Analisis / Factores relevantes */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
              Análisis y factores relevantes
            </h2>
            <Field label="Análisis DOFA">
              <textarea
                rows={3}
                value={form.analisis_dofa}
                onChange={(e) => setField("analisis_dofa", e.target.value)}
                className={inputClass}
              />
            </Field>
            <Field label="Factores relevantes / Insights">
              <textarea
                rows={3}
                value={form.factores_relevantes}
                onChange={(e) => setField("factores_relevantes", e.target.value)}
                className={inputClass}
              />
            </Field>
          </section>

          {/* Clasificacion proveedores + Kraljic */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
              Clasificación de proveedores
            </h2>
            <TagInput
              label="Estratégicos"
              values={form.clasificacion_proveedores.estrategicos}
              onChange={(v) => setField("clasificacion_proveedores.estrategicos", v)}
            />
            <TagInput
              label="Clave"
              values={form.clasificacion_proveedores.clave}
              onChange={(v) => setField("clasificacion_proveedores.clave", v)}
            />
            <TagInput
              label="Tácticos"
              values={form.clasificacion_proveedores.tacticos}
              onChange={(v) => setField("clasificacion_proveedores.tacticos", v)}
            />

            <Field label="Cuadrante Kraljic" hint="Clasificación de la familia según la matriz de Kraljic.">
              <select
                value={form.kraljic || ""}
                onChange={(e) => setField("kraljic", e.target.value)}
                className={inputClass}
              >
                <option value="">Sin definir</option>
                <option value="estrategico">Estratégico</option>
                <option value="cuello_de_botella">Cuello de botella</option>
                <option value="apalancamiento">Apalancamiento</option>
                <option value="rutinario">Rutinario</option>
              </select>
            </Field>
          </section>

          {/* Actores principales / Premisas */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
              Actores y negociación
            </h2>
            <Field label="Actores principales" hint="Principales proveedores y productos que maneja.">
              <textarea
                rows={3}
                value={form.actores_principales}
                onChange={(e) => setField("actores_principales", e.target.value)}
                className={inputClass}
              />
            </Field>
            <Field label="Premisas de negociación">
              <textarea
                rows={3}
                value={form.premisas_negociacion}
                onChange={(e) => setField("premisas_negociacion", e.target.value)}
                className={inputClass}
              />
            </Field>
          </section>

          {/* Clasificacion cliente interno */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
              Clasificación cliente interno
            </h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {["estrategicos", "clave", "tacticos"].map((key) => (
                <div key={key} className="rounded-lg border border-surface-border p-3">
                  <p className="mb-2 text-xs font-semibold capitalize text-slate-600">{key}</p>
                  <Field label="Spend ($)">
                    <input
                      type="number"
                      step="any"
                      value={form.clasificacion_cliente_interno[key].spend}
                      onChange={(e) =>
                        setField(`clasificacion_cliente_interno.${key}.spend`, Number(e.target.value))
                      }
                      className={inputClass}
                    />
                  </Field>
                  <Field label="# OCs">
                    <input
                      type="number"
                      value={form.clasificacion_cliente_interno[key].ocs}
                      onChange={(e) =>
                        setField(`clasificacion_cliente_interno.${key}.ocs`, Number(e.target.value))
                      }
                      className={inputClass}
                    />
                  </Field>
                </div>
              ))}
            </div>
          </section>

          {/* Subfamilias / Estrategia */}
          <section className="rounded-xl2 border border-surface-border bg-white p-5 shadow-card">
            <h2 className="mb-4 text-sm font-bold uppercase tracking-wide text-brand-red">
              Subfamilias y estrategia
            </h2>
            <Field label="Subfamilias" hint="Indique las subfamilias asociadas.">
              <textarea
                rows={2}
                value={form.subfamilias}
                onChange={(e) => setField("subfamilias", e.target.value)}
                className={inputClass}
              />
            </Field>
            <Field label="Estrategia a aplicar">
              <textarea
                rows={3}
                value={form.estrategia_aplicar}
                onChange={(e) => setField("estrategia_aplicar", e.target.value)}
                className={inputClass}
              />
            </Field>
          </section>

          <div className="flex justify-end gap-3 pb-10">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="rounded-lg border border-surface-border px-5 py-2.5 text-sm font-medium text-slate-600 hover:bg-surface"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 rounded-lg bg-navy px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-light disabled:opacity-60"
            >
              {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
              Guardar ficha
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
