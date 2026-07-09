const KRALJIC_LABELS = {
  estrategico: "Estratégico",
  cuello_de_botella: "Cuello de botella",
  apalancamiento: "Apalancamiento",
  rutinario: "Rutinario",
};

const ESTADO_LABELS = {
  borrador: "Borrador",
  activa: "Activa",
  archivada: "Archivada",
};

function SectionHeader({ children }) {
  return (
    <div className="rounded-t-md bg-brand-red px-3 py-1.5">
      <p className="text-[11px] font-bold uppercase tracking-wide text-white">{children}</p>
    </div>
  );
}

function SectionBox({ title, children, className = "" }) {
  return (
    <div className={`flex flex-col ${className}`}>
      <SectionHeader>{title}</SectionHeader>
      <div className="flex-1 rounded-b-md border border-t-0 border-surface-border bg-white p-3 text-[12.5px] leading-relaxed text-slate-700">
        {children}
      </div>
    </div>
  );
}

function EmptyText({ children }) {
  return <p className="italic text-slate-400">{children || "Sin información registrada."}</p>;
}

function Tags({ items }) {
  if (!items || items.length === 0) return <EmptyText />;
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((item, idx) => (
        <span
          key={idx}
          className="rounded-full bg-navy/5 px-2.5 py-0.5 text-[11.5px] font-medium text-navy"
        >
          {item}
        </span>
      ))}
    </div>
  );
}

export default function FichaPreview({ ficha }) {
  if (!ficha) return null;

  const status = ficha.status || {};
  const cp = ficha.clasificacion_proveedores || {};
  const cci = ficha.clasificacion_cliente_interno || {};

  return (
    <div
      id="ficha-imprimible"
      className="mx-auto w-full max-w-5xl overflow-hidden rounded-xl2 border border-surface-border bg-white shadow-panel"
    >
      {/* Encabezado navy */}
      <div className="bg-navy px-6 py-5 text-center">
        <h1 className="text-xl font-extrabold tracking-wide text-white">
          FASE 1 – ESTANDARIZACIÓN
        </h1>
        <p className="mt-0.5 text-sm text-white/80">Ficha Familias</p>
      </div>

      <div className="p-5">
        {/* Estado / metadatos */}
        <div className="mb-4 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
          <span>
            Ficha #{ficha.id} · Creada por {ficha.creador_nombre || "—"}
          </span>
          <span className="rounded-full bg-navy/5 px-3 py-1 font-semibold text-navy">
            {ESTADO_LABELS[ficha.estado] || ficha.estado}
          </span>
        </div>

        {/* Linea de abastecimiento / Lider */}
        <div className="mb-4 grid grid-cols-1 gap-3 md:grid-cols-3">
          <div className="flex flex-col md:col-span-2">
            <SectionHeader>Línea de abastecimiento:</SectionHeader>
            <div className="rounded-b-md border border-t-0 border-surface-border bg-white p-3">
              <p className="text-sm font-semibold text-slate-800">
                {ficha.linea_abastecimiento || <EmptyText>Sin línea definida</EmptyText>}
              </p>
              <p className="mt-1 text-xs italic text-slate-500">Descripción de familia:</p>
              <p className="text-[12.5px] text-slate-600">
                {ficha.descripcion_familia || <EmptyText />}
              </p>
            </div>
          </div>
          <div className="flex flex-col">
            <SectionHeader>Líder:</SectionHeader>
            <div className="flex flex-1 items-center rounded-b-md border border-t-0 border-surface-border bg-white p-3">
              <p className="text-sm font-semibold text-slate-800">
                {ficha.lider || <EmptyText>Sin líder asignado</EmptyText>}
              </p>
            </div>
          </div>
        </div>

        {/* Grid principal de 3 columnas */}
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
          {/* Columna izquierda */}
          <div className="flex flex-col gap-3">
            <SectionBox title="Status">
              <ul className="space-y-1">
                <li>
                  <span className="font-semibold text-slate-800">Spend 2025:</span> ${" "}
                  {Number(status.spend_2025 || 0).toLocaleString("es-CO")}
                </li>
                <li>
                  <span className="font-semibold text-slate-800"># Proveedores:</span>{" "}
                  {status.num_proveedores || 0}
                </li>
                <li>
                  <span className="font-semibold text-slate-800">Spend bajo control:</span> ${" "}
                  {Number(status.spend_under_control || 0).toLocaleString("es-CO")}
                </li>
                <li>
                  <span className="font-semibold text-slate-800"># Proveedores SUC:</span>{" "}
                  {status.num_proveedores_suc || 0}
                </li>
              </ul>
            </SectionBox>

            <SectionBox title="Clasificación proveedores">
              <div className="space-y-2">
                <div>
                  <p className="mb-1 text-[11px] font-semibold uppercase text-slate-500">Estratégicos</p>
                  <Tags items={cp.estrategicos} />
                </div>
                <div>
                  <p className="mb-1 text-[11px] font-semibold uppercase text-slate-500">Clave</p>
                  <Tags items={cp.clave} />
                </div>
                <div>
                  <p className="mb-1 text-[11px] font-semibold uppercase text-slate-500">Tácticos</p>
                  <Tags items={cp.tacticos} />
                </div>
              </div>
            </SectionBox>

            <SectionBox title="Clasificación cliente interno" className="flex-1">
              <table className="w-full text-[12px]">
                <thead>
                  <tr className="text-left text-slate-500">
                    <th className="pb-1 font-semibold"> </th>
                    <th className="pb-1 font-semibold">Spend</th>
                    <th className="pb-1 font-semibold"># OCs</th>
                  </tr>
                </thead>
                <tbody>
                  {["estrategicos", "clave", "tacticos"].map((key) => (
                    <tr key={key} className="border-t border-surface-border">
                      <td className="py-1 font-medium capitalize text-slate-700">{key}</td>
                      <td className="py-1">${Number(cci[key]?.spend || 0).toLocaleString("es-CO")}</td>
                      <td className="py-1">{cci[key]?.ocs || 0}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </SectionBox>
          </div>

          {/* Columna central */}
          <div className="flex flex-col gap-3">
            <SectionBox title="Análisis">
              <p className="mb-1 text-[11px] font-semibold uppercase text-slate-500">Análisis DOFA:</p>
              <p className="whitespace-pre-line">{ficha.analisis_dofa || <EmptyText />}</p>
            </SectionBox>

            <SectionBox title="Kraljic">
              <p className="mb-1 text-[11px] font-semibold uppercase text-slate-500">Cuadrante:</p>
              {ficha.kraljic ? (
                <span className="inline-block rounded-full bg-brand-red/10 px-3 py-1 text-xs font-bold text-brand-red">
                  {KRALJIC_LABELS[ficha.kraljic] || ficha.kraljic}
                </span>
              ) : (
                <EmptyText>Sin definir</EmptyText>
              )}
            </SectionBox>

            <SectionBox title="Actores principales">
              <p className="mb-1 text-[11px] italic text-slate-500">
                Principales proveedores y productos que maneja:
              </p>
              <p className="whitespace-pre-line">{ficha.actores_principales || <EmptyText />}</p>
            </SectionBox>

            <SectionBox title="Subfamilias" className="flex-1">
              <p className="mb-1 text-[11px] italic text-slate-500">Indique las subfamilias:</p>
              <p className="whitespace-pre-line">{ficha.subfamilias || <EmptyText />}</p>
            </SectionBox>
          </div>

          {/* Columna derecha */}
          <div className="flex flex-col gap-3">
            <SectionBox title="Factores relevantes">
              <p className="mb-1 text-[11px] italic text-slate-500">Insights:</p>
              <p className="whitespace-pre-line">{ficha.factores_relevantes || <EmptyText />}</p>
            </SectionBox>

            <SectionBox title="Premisas de negociación" className="flex-1">
              <p className="mb-1 text-[11px] italic text-slate-500">
                Premisas a negociar en la familia:
              </p>
              <p className="whitespace-pre-line">{ficha.premisas_negociacion || <EmptyText />}</p>
            </SectionBox>

            <SectionBox title="Estrategia a aplicar">
              <p className="whitespace-pre-line">{ficha.estrategia_aplicar || <EmptyText />}</p>
            </SectionBox>
          </div>
        </div>
      </div>
    </div>
  );
}
