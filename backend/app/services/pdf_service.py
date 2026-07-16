import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.models.familia import Familia
from app.models.revision_estrategica import RevisionEstrategica

NAVY = HexColor("#0B2A5B")
RED = HexColor("#E2231A")
GRAY_BAR = HexColor("#4B5563")
BADGE_GRAY = HexColor("#9CA3AF")
LIGHT_GRAY = HexColor("#F4F5F7")
BORDER_GRAY = HexColor("#D5D9E0")
WHITE = HexColor("#FFFFFF")
TEXT_DARK = HexColor("#1F2937")
TABLE_HEADER_BG = HexColor("#FADBD8")

PAGE_W, PAGE_H = A4
MARGIN = 12 * mm

KRALJIC_LABELS = {
    "estrategico": "Estratégico",
    "cuello_de_botella": "Cuello de botella",
    "apalancamiento": "Apalancamiento",
    "rutinario": "Rutinario",
}

NIVEL_PODER_LABELS = {
    "bajo": "Bajo",
    "alto": "Alto",
}

ANIOS = ("2026", "2027", "2028")


def _wrap_text(c: canvas.Canvas, text: str, font: str, size: int, max_width: float) -> list[str]:
    """Envuelve texto plano en lineas que caben en max_width, respetando saltos manuales."""
    lines: list[str] = []
    for raw_line in (text or "").split("\n"):
        words = raw_line.split(" ")
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if stringWidth(trial, font, size) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        lines.append(current)
    return lines


def _fit_text(text: str, font: str, size: int, max_width: float) -> str:
    """Trunca un texto de una sola linea con '...' si no cabe en max_width."""
    if stringWidth(text, font, size) <= max_width:
        return text
    ellipsis = "..."
    while text and stringWidth(text + ellipsis, font, size) > max_width:
        text = text[:-1]
    return (text + ellipsis) if text else ellipsis


class FichaPDFBuilder:
    """Construye el PDF de 3 paginas de una ficha: Donde estamos / Donde queremos
    llegar / Que resultados esperamos, replicando el layout visual oficial."""

    def __init__(self, familia: Familia, revision: RevisionEstrategica):
        self.familia = familia
        self.revision = revision
        self.buffer = io.BytesIO()
        self.c = canvas.Canvas(self.buffer, pagesize=A4)

    def build(self) -> bytes:
        self._draw_pagina_1()
        self.c.showPage()
        self._draw_pagina_2()
        self.c.showPage()
        self._draw_pagina_3()
        self.c.save()
        self.buffer.seek(0)
        return self.buffer.read()

    # =========================================================================
    # HELPERS COMUNES
    # =========================================================================
    def _draw_header(self, page_num: int, subtitulo: str):
        c = self.c
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 13 * mm, "FASE 1 \u2013 ESTANDARIZACI\u00d3N")
        c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 20 * mm, f"P\u00e1gina {page_num} de 3 \u00b7 {subtitulo}")

    def _draw_badge(self, text: str, top_y: float) -> float:
        """Dibuja la etiqueta gris de contexto ('Donde estamos?', etc). Devuelve el nuevo top."""
        c = self.c
        badge_h = 5.5 * mm
        badge_w = stringWidth(text, "Helvetica-Bold", 8) + 6 * mm
        y = top_y - badge_h
        c.setFillColor(BADGE_GRAY)
        c.roundRect(MARGIN, y, badge_w, badge_h, 1.5 * mm, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(MARGIN + badge_w / 2, y + 1.9 * mm, text)
        return y - 2.5 * mm

    def _section(self, x: float, y_top: float, w: float, h: float, title: str, lines: list[str]):
        """Dibuja un bloque: barra roja con titulo + caja blanca con lineas de texto."""
        c = self.c
        bar_h = min(6 * mm, h * 0.35)
        c.setFillColor(RED)
        c.rect(x, y_top - bar_h, w, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 7.5)
        titulo_ajustado = _fit_text(title, "Helvetica-Bold", 7.5, w - 4 * mm)
        c.drawString(x + 2 * mm, y_top - bar_h + bar_h / 2 - 2, titulo_ajustado)

        box_h = h - bar_h
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(x, y_top - h, w, box_h, fill=1, stroke=1)

        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica", 7)
        text_y = y_top - bar_h - 3.6 * mm
        line_h = 3.2 * mm
        max_lines = max(1, int(box_h / line_h) - 1)
        rendered = 0
        for line in lines:
            wrapped = _wrap_text(c, line, "Helvetica", 7, w - 4 * mm)
            for wl in wrapped:
                if rendered >= max_lines:
                    break
                c.drawString(x + 2 * mm, text_y, wl)
                text_y -= line_h
                rendered += 1
            if rendered >= max_lines:
                break
        return y_top - h

    def _bar_only(self, x: float, y_top: float, w: float, bar_h: float, title: str, color) -> float:
        """Dibuja solo una barra de titulo (sin caja blanca debajo). Usada para encabezados de columna."""
        c = self.c
        c.setFillColor(color)
        c.rect(x, y_top - bar_h, w, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + w / 2, y_top - bar_h + bar_h / 2 - 2.5, title)
        return y_top - bar_h

    def _draw_columna_apilada(self, x: float, y_top: float, w: float, h: float, items: list[tuple[str, str]]):
        """Dibuja N cajas del mismo ancho apiladas verticalmente con el mismo espaciado."""
        n = len(items)
        gap = 2 * mm
        box_h = (h - (n - 1) * gap) / n
        y = y_top
        for titulo, texto in items:
            y = self._section(x, y, w, box_h, titulo, [texto])
            y -= gap

    # =========================================================================
    # PAGINA 1 - DONDE ESTAMOS
    # =========================================================================
    def _draw_pagina_1(self):
        self._draw_header(1, "D\u00f3nde estamos")
        top = PAGE_H - 26 * mm - 3 * mm
        top = self._draw_badge("\u00bfD\u00f3nde estamos?", top)
        top = self._draw_encabezado_ficha(top)
        self._draw_dos_columnas_pagina_1(top)

    def _draw_encabezado_ficha(self, top: float) -> float:
        c = self.c
        f = self.familia
        bar_h = 7 * mm
        col_split = PAGE_W * 0.68

        c.setFillColor(RED)
        c.rect(MARGIN, top - bar_h, PAGE_W - 2 * MARGIN, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        linea_txt = _fit_text(
            f"L\u00cdNEA DE ABASTECIMIENTO: {f.linea_abastecimiento or ''}",
            "Helvetica-Bold", 8.5, col_split - MARGIN - 4 * mm,
        )
        c.drawString(MARGIN + 2 * mm, top - bar_h + 2.3 * mm, linea_txt)
        lider_txt = _fit_text(
            f"L\u00cdDER: {f.lider or ''}", "Helvetica-Bold", 8.5, PAGE_W - MARGIN - col_split - 4 * mm
        )
        c.drawString(col_split + 2 * mm, top - bar_h + 2.3 * mm, lider_txt)

        desc_top = top - bar_h
        desc_h = 12 * mm
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(MARGIN, desc_top - desc_h, PAGE_W - 2 * MARGIN, desc_h, fill=1, stroke=1)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(MARGIN + 2 * mm, desc_top - 4 * mm, "Descripci\u00f3n de familia:")
        c.setFont("Helvetica", 8)
        wrapped = _wrap_text(c, f.descripcion_familia or "", "Helvetica", 8, PAGE_W - 2 * MARGIN - 4 * mm)
        ty = desc_top - 8 * mm
        for wl in wrapped[:2]:
            c.drawString(MARGIN + 2 * mm, ty, wl)
            ty -= 3.6 * mm

        return desc_top - desc_h - 3 * mm

    def _draw_dos_columnas_pagina_1(self, top: float):
        bottom = MARGIN
        gap = 4 * mm
        col_w = (PAGE_W - 2 * MARGIN - gap) / 2
        x_left = MARGIN
        x_right = MARGIN + col_w + gap

        self._draw_columna_interna(x_left, top, col_w, bottom)
        self._draw_columna_externa(x_right, top, col_w, bottom)

    def _draw_columna_interna(self, x: float, top: float, w: float, bottom: float):
        f = self.familia
        gap = 3 * mm

        y = self._bar_only(x, top, w, 6 * mm, "AN\u00c1LISIS INTERNO", GRAY_BAR)
        y -= gap

        matrix_h = (top - bottom) * 0.24
        y = self._matriz_analisis_interno(x, y, w, matrix_h, f.analisis_interno or {})
        y -= gap

        # dos sub-columnas para el resto del espacio disponible
        sub_gap = 3 * mm
        half_w = (w - sub_gap) / 2
        x_l, x_r = x, x + half_w + sub_gap
        usable_h = (y - bottom) - 2 * sub_gap

        status = f.status or {}
        status_lines = [f"# Proveedores: {status.get('num_proveedores', 0)}", f"# OCs: {status.get('num_ocs', 0)}"]
        cp = f.clasificacion_proveedores or {}
        cp_lines = [
            "Apalancados: " + ", ".join(cp.get("apalancados", []) or []),
            "Estrat\u00e9gicos: " + ", ".join(cp.get("estrategicos", []) or []),
            "Rutinarios: " + ", ".join(cp.get("rutinarios", []) or []),
            "Cuello de botella: " + ", ".join(cp.get("cuello_de_botella", []) or []),
        ]
        cci = f.clasificacion_cliente_interno or {}
        cci_lines = []
        for label, key in (("Recurrentes", "recurrentes"), ("Ocasionales", "ocasionales")):
            item = cci.get(key, {}) or {}
            cci_lines.append(f"{label} - Spend: {item.get('spend', 0)} | # OCs: {item.get('ocs', 0)}")

        yl = y
        yl = self._section(x_l, yl, half_w, usable_h * 0.15, "STATUS", status_lines)
        yl -= sub_gap
        yl = self._section(x_l, yl, half_w, usable_h * 0.55, "CLASIFICACI\u00d3N PROVEEDORES", cp_lines)
        yl -= sub_gap
        self._section(x_l, yl, half_w, usable_h * 0.30, "CLASIFICACI\u00d3N CLIENTE INTERNO", cci_lines)

        kraljic_label = KRALJIC_LABELS.get(f.kraljic.value, f.kraljic.value) if f.kraljic else "Sin definir"
        yr = y
        yr = self._section(x_r, yr, half_w, usable_h * 0.15, "SUBFAMILIAS", [f.subfamilias or "Sin informaci\u00f3n."])
        yr -= sub_gap
        yr = self._section(
            x_r, yr, half_w, usable_h * 0.70, "PREMISAS DE NEGOCIACI\u00d3N", [f.premisas_negociacion or "Sin informaci\u00f3n."]
        )
        yr -= sub_gap
        self._section(x_r, yr, half_w, usable_h * 0.15, "KRALJIC DE LA FAMILIA", [f"Cuadrante: {kraljic_label}"])

    def _matriz_analisis_interno(self, x: float, y_top: float, w: float, h: float, ai: dict) -> float:
        """Tabla Y-1 / Y / Y+1 con las filas Spend, % Cobertura, Spend U Contr."""
        c = self.c
        label_w = w * 0.34
        val_w = (w - label_w) / 3
        row_h = h / 4  # fila de encabezado + 3 filas de datos

        # Titulo del bloque
        c.setFillColor(RED)
        c.rect(x, y_top - 5 * mm, w, 5 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(x + 2 * mm, y_top - 5 * mm + 1.5 * mm, "SPEND / % COBERTURA / SPEND U. CONTR.")
        grid_top = y_top - 5 * mm
        row_h = (h - 5 * mm) / 4

        # Fila de encabezado (Y-1, Y, Y+1)
        c.setFillColor(TABLE_HEADER_BG)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(x, grid_top - row_h, label_w, row_h, fill=1, stroke=1)
        for i, hdr in enumerate(("Y-1", "Y", "Y+1")):
            cx = x + label_w + i * val_w
            c.setFillColor(TABLE_HEADER_BG)
            c.rect(cx, grid_top - row_h, val_w, row_h, fill=1, stroke=1)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawCentredString(cx + val_w / 2, grid_top - row_h + row_h / 2 - 2.5, hdr)

        filas = [("Spend", "spend"), ("% Cobertura", "pct_cobertura"), ("Spend U Contr", "spend_under_control")]
        ry = grid_top - row_h
        for label, key in filas:
            serie = ai.get(key, {}) or {}
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER_GRAY)
            c.rect(x, ry - row_h, label_w, row_h, fill=1, stroke=1)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(x + 1.5 * mm, ry - row_h + row_h / 2 - 2.2, label)

            valores = [serie.get("y_menos_1", 0), serie.get("y", 0), serie.get("y_mas_1", 0)]
            for i, valor in enumerate(valores):
                cx = x + label_w + i * val_w
                c.setFillColor(WHITE)
                c.setStrokeColor(BORDER_GRAY)
                c.rect(cx, ry - row_h, val_w, row_h, fill=1, stroke=1)
                c.setFillColor(TEXT_DARK)
                c.setFont("Helvetica", 7.5)
                c.drawCentredString(cx + val_w / 2, ry - row_h + row_h / 2 - 2.5, str(valor))
            ry -= row_h

        return y_top - h

    def _dual_box(
        self, x: float, y_top: float, w: float, h: float, title: str,
        left_label: str, left_text: str, right_label: str, right_text: str,
    ) -> float:
        """Bloque con titulo unico y dos cajas lado a lado (usado para Factores Relevantes)."""
        c = self.c
        bar_h = 6 * mm
        c.setFillColor(RED)
        c.rect(x, y_top - bar_h, w, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 2 * mm, y_top - bar_h + 1.8 * mm, title)

        box_h = h - bar_h
        cell_gap = 2 * mm
        half_w = (w - cell_gap) / 2

        for i, (lbl, txt) in enumerate(((left_label, left_text), (right_label, right_text))):
            bx = x + i * (half_w + cell_gap)
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER_GRAY)
            c.rect(bx, y_top - h, half_w, box_h, fill=1, stroke=1)

            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Oblique", 6.5)
            ly = y_top - bar_h - 3.2 * mm
            for wl in _wrap_text(c, f"{lbl}:", "Helvetica-Oblique", 6.5, half_w - 3 * mm):
                c.drawString(bx + 1.5 * mm, ly, wl)
                ly -= 2.8 * mm

            c.setFont("Helvetica", 7)
            max_lines = max(1, int((box_h - (y_top - bar_h - ly)) / (3 * mm)))
            for wl in _wrap_text(c, txt, "Helvetica", 7, half_w - 3 * mm)[:max_lines]:
                c.drawString(bx + 1.5 * mm, ly, wl)
                ly -= 3 * mm

        return y_top - h

    def _dofa_grid(self, x: float, y_top: float, w: float, h: float, dofa: dict) -> float:
        """Bloque ANALISIS DOFA como matriz 2x2: Debilidades|Oportunidades / Fortalezas|Amenazas."""
        c = self.c
        bar_h = 6 * mm
        c.setFillColor(RED)
        c.rect(x, y_top - bar_h, w, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 2 * mm, y_top - bar_h + 1.8 * mm, "AN\u00c1LISIS DOFA")

        grid_top = y_top - bar_h
        grid_h = h - bar_h
        cell_gap = 2 * mm
        cell_w = (w - cell_gap) / 2
        cell_h = (grid_h - cell_gap) / 2

        celdas = [
            ("Debilidades", dofa.get("debilidades", "") or "Sin informaci\u00f3n.", x, grid_top),
            ("Oportunidades", dofa.get("oportunidades", "") or "Sin informaci\u00f3n.", x + cell_w + cell_gap, grid_top),
            ("Fortalezas", dofa.get("fortalezas", "") or "Sin informaci\u00f3n.", x, grid_top - cell_h - cell_gap),
            (
                "Amenazas", dofa.get("amenazas", "") or "Sin informaci\u00f3n.",
                x + cell_w + cell_gap, grid_top - cell_h - cell_gap,
            ),
        ]
        for label, texto, cx, cy in celdas:
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER_GRAY)
            c.rect(cx, cy - cell_h, cell_w, cell_h, fill=1, stroke=1)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(cx + 1.5 * mm, cy - 4 * mm, label)
            c.setFont("Helvetica", 6.8)
            ty = cy - 7.5 * mm
            max_lines = max(1, int((cell_h - 6 * mm) / (3 * mm)))
            for wl in _wrap_text(c, texto, "Helvetica", 6.8, cell_w - 3 * mm)[:max_lines]:
                c.drawString(cx + 1.5 * mm, ty, wl)
                ty -= 3 * mm

        return y_top - h

    def _draw_columna_externa(self, x: float, top: float, w: float, bottom: float):
        f = self.familia
        gap = 3 * mm

        y = self._bar_only(x, top, w, 6 * mm, "AN\u00c1LISIS EXTERNO", GRAY_BAR)
        y -= gap

        usable_h = (y - bottom) - 3 * gap  # 4 bloques principales -> 3 espacios entre ellos
        h_factores = usable_h * 0.20
        h_actores_row = usable_h * 0.18
        h_dofa = usable_h * 0.40
        h_estrategia = usable_h * 0.22

        fr = f.factores_relevantes or {}
        y = self._dual_box(
            x, y, w, h_factores, "FACTORES RELEVANTES",
            "Insights", fr.get("insights", "") or "Sin informaci\u00f3n.",
            "Indicadores Econ\u00f3micos y Financieros",
            fr.get("indicadores_economicos_financieros", "") or "Sin informaci\u00f3n.",
        )
        y -= gap

        actores_w = w * 0.62
        poder_w = w - actores_w - 3 * mm
        self._section(x, y, actores_w, h_actores_row, "ACTORES PRINCIPALES", [f.actores_principales or "Sin informaci\u00f3n."])
        pn = f.poder_negociacion or {}
        pn_lines = [
            f"Veolia: {NIVEL_PODER_LABELS.get(pn.get('veolia'), 'Sin definir')}",
            f"Proveedor: {NIVEL_PODER_LABELS.get(pn.get('proveedor'), 'Sin definir')}",
        ]
        self._section(x + actores_w + 3 * mm, y, poder_w, h_actores_row, "PODER DE NEGOCIACI\u00d3N", pn_lines)
        y -= h_actores_row
        y -= gap

        y = self._dofa_grid(x, y, w, h_dofa, f.analisis_dofa or {})
        y -= gap

        self._section(x, y, w, h_estrategia, "ESTRATEGIA A APLICAR", [f.estrategia_aplicar or "Sin informaci\u00f3n."])

    # =========================================================================
    # PAGINA 2 - DONDE QUEREMOS LLEGAR
    # =========================================================================
    def _draw_pagina_2(self):
        self._draw_header(2, "D\u00f3nde queremos llegar")
        top = PAGE_H - 26 * mm - 3 * mm
        top = self._draw_badge("\u00bfD\u00f3nde queremos llegar?", top)

        r = self.revision
        gap = 3 * mm

        obj_h = 20 * mm
        y = self._section(
            MARGIN, top, PAGE_W - 2 * MARGIN, obj_h,
            "OBJETIVO ESTRAT\u00c9GICO DE LA REVISI\u00d3N",
            [r.objetivo_estrategico or "Sin informaci\u00f3n."],
        )
        y -= gap

        roadmap_block_h = 26 * mm  # barra + 3 cajas del roadmap, reservado abajo
        ejes_top = y
        ejes_bottom = MARGIN + roadmap_block_h + gap
        ejes_h = ejes_top - ejes_bottom

        n_cols = 5
        col_gap = 2.5 * mm
        col_w = (PAGE_W - 2 * MARGIN - (n_cols - 1) * col_gap) / n_cols

        ejes = r.ejes_estrategicos or {}
        riesgo = ejes.get("riesgo", {}) or {}
        innovacion = ejes.get("innovacion", {}) or {}
        asg = ejes.get("ambiental_social_gobernanza", {}) or {}

        x0 = MARGIN
        self._section(
            x0, ejes_top, col_w, ejes_h, "PERFORMANCE ECON\u00d3MICO",
            [ejes.get("performance_economico", "") or "Sin informaci\u00f3n."],
        )

        x1c = x0 + col_w + col_gap
        self._section(
            x1c, ejes_top, col_w, ejes_h, "PERFORMANCE OPERACIONAL",
            [ejes.get("performance_operacional", "") or "Sin informaci\u00f3n."],
        )

        x2c = x1c + col_w + col_gap
        self._draw_columna_apilada(x2c, ejes_top, col_w, ejes_h, [
            ("COMPLIANCE", riesgo.get("compliance", "") or "Sin informaci\u00f3n."),
            ("FINANCIERO", riesgo.get("financiero", "") or "Sin informaci\u00f3n."),
            ("OPERATIVO", riesgo.get("operativo", "") or "Sin informaci\u00f3n."),
            ("AMBIENTAL Y PSS", riesgo.get("ambiental_pss", "") or "Sin informaci\u00f3n."),
        ])

        x3c = x2c + col_w + col_gap
        self._draw_columna_apilada(x3c, ejes_top, col_w, ejes_h, [
            ("INNOVACI\u00d3N", innovacion.get("general", "") or "Sin informaci\u00f3n."),
            ("CRECIMIENTO INGRESOS", innovacion.get("crecimiento_ingresos", "") or "Sin informaci\u00f3n."),
        ])

        x4c = x3c + col_w + col_gap
        self._draw_columna_apilada(x4c, ejes_top, col_w, ejes_h, [
            ("DECARBONIZACI\u00d3N", asg.get("decarbonizacion", "") or "Sin informaci\u00f3n."),
            ("ECONOM\u00cdA CIRCULAR", asg.get("economia_circular", "") or "Sin informaci\u00f3n."),
            ("CREACI\u00d3N DE VALOR TERRITORIAL", asg.get("creacion_valor_territorial", "") or "Sin informaci\u00f3n."),
            ("DERECHOS HUMANOS Y COMPLIANCE", asg.get("derechos_humanos_compliance", "") or "Sin informaci\u00f3n."),
        ])

        # Roadmap a 3 anios: bloque independiente, 3 cajas identicas
        roadmap = r.roadmap or {}
        roadmap_top = ejes_bottom - gap
        bar_h = 6 * mm
        c = self.c
        c.setFillColor(RED)
        c.rect(MARGIN, roadmap_top - bar_h, PAGE_W - 2 * MARGIN, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN + 2 * mm, roadmap_top - bar_h + 1.8 * mm, "ROADMAP A 3 A\u00d1OS")

        year_gap = 3 * mm
        year_col_w = (PAGE_W - 2 * MARGIN - 2 * year_gap) / 3
        year_box_h = roadmap_top - bar_h - MARGIN
        for i, anio in enumerate(ANIOS):
            x = MARGIN + i * (year_col_w + year_gap)
            self._section(x, roadmap_top - bar_h, year_col_w, year_box_h, anio, [roadmap.get(anio, "") or "Sin informaci\u00f3n."])

    # =========================================================================
    # PAGINA 3 - QUE RESULTADOS ESPERAMOS (sin cambios, ya validada)
    # =========================================================================
    def _draw_pagina_3(self):
        self._draw_header(3, "Qu\u00e9 resultados esperamos")
        self._draw_matriz_beneficios()

    def _draw_matriz_beneficios(self):
        c = self.c
        beneficios = self.revision.beneficios_esperados or {}

        ejes_labels = [
            ("spend_under_control", "Spend Under Control"),
            ("performance_economico", "Performance Econ\u00f3mico"),
            ("performance_operativo", "Performance Operativo"),
            ("riesgo", "Riesgo"),
            ("innovacion", "Innovaci\u00f3n"),
            ("crecimiento_ingresos", "Crecimiento Ingresos"),
            ("ambiental_social_gobernanza", "Ambiental-Social-Gobernanza"),
        ]

        top = PAGE_H - 26 * mm - 4 * mm
        bar_h = 7 * mm
        c.setFillColor(RED)
        c.rect(MARGIN, top - bar_h, PAGE_W - 2 * MARGIN, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN + 2 * mm, top - bar_h + 2 * mm, "BENEFICIOS ESPERADOS A 3 A\u00d1OS")

        table_top = top - bar_h - 3 * mm
        table_bottom = MARGIN
        table_h = table_top - table_bottom

        label_col_w = (PAGE_W - 2 * MARGIN) * 0.30
        year_col_w = (PAGE_W - 2 * MARGIN - label_col_w) / 3

        header_h = 9 * mm
        row_h = (table_h - header_h) / len(ejes_labels)

        c.setFillColor(TABLE_HEADER_BG)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(MARGIN, table_top - header_h, label_col_w, header_h, fill=1, stroke=1)
        for i, anio in enumerate(ANIOS):
            x = MARGIN + label_col_w + i * year_col_w
            c.rect(x, table_top - header_h, year_col_w, header_h, fill=1, stroke=1)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(x + year_col_w / 2, table_top - header_h + header_h / 2 - 3, anio)
            c.setFillColor(TABLE_HEADER_BG)

        row_top = table_top - header_h
        for key, label in ejes_labels:
            valores = beneficios.get(key, {}) or {}

            c.setFillColor(LIGHT_GRAY)
            c.setStrokeColor(BORDER_GRAY)
            c.rect(MARGIN, row_top - row_h, label_col_w, row_h, fill=1, stroke=1)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica-Bold", 8)
            wrapped_label = _wrap_text(c, label, "Helvetica-Bold", 8, label_col_w - 4 * mm)
            ly = row_top - 4 * mm
            for wl in wrapped_label:
                c.drawString(MARGIN + 2 * mm, ly, wl)
                ly -= 3.4 * mm

            for i, anio in enumerate(ANIOS):
                x = MARGIN + label_col_w + i * year_col_w
                c.setFillColor(WHITE)
                c.setStrokeColor(BORDER_GRAY)
                c.rect(x, row_top - row_h, year_col_w, row_h, fill=1, stroke=1)
                c.setFillColor(TEXT_DARK)
                c.setFont("Helvetica", 7.5)
                texto = valores.get(anio, "") or "-"
                wrapped = _wrap_text(c, texto, "Helvetica", 7.5, year_col_w - 3 * mm)
                ty = row_top - 4 * mm
                max_lines = int(row_h / (3.2 * mm))
                for wl in wrapped[:max_lines]:
                    c.drawString(x + 1.5 * mm, ty, wl)
                    ty -= 3.2 * mm

            row_top -= row_h


def generate_familia_pdf(familia: Familia, revision: RevisionEstrategica) -> bytes:
    return FichaPDFBuilder(familia, revision).build()