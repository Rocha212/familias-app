import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.models.familia import Familia

NAVY = HexColor("#0B2A5B")
RED = HexColor("#E2231A")
LIGHT_GRAY = HexColor("#F4F5F7")
BORDER_GRAY = HexColor("#D5D9E0")
WHITE = HexColor("#FFFFFF")
TEXT_DARK = HexColor("#1F2937")

PAGE_W, PAGE_H = A4
MARGIN = 12 * mm


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


class FichaPDFBuilder:
    """Construye el PDF de una ficha replicando el layout visual de 3 columnas."""

    def __init__(self, familia: Familia):
        self.familia = familia
        self.buffer = io.BytesIO()
        self.c = canvas.Canvas(self.buffer, pagesize=A4)

    def build(self) -> bytes:
        self._draw_header()
        self._draw_encabezado()
        self._draw_grid()
        self.c.save()
        self.buffer.seek(0)
        return self.buffer.read()

    # ---- bloques principales -------------------------------------------------
    def _draw_header(self):
        c = self.c
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 13 * mm, "FASE 1 \u2013 ESTANDARIZACI\u00d3N")
        c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 20 * mm, "Ficha Familias")

    def _draw_encabezado(self):
        c = self.c
        top = PAGE_H - 26 * mm
        bar_h = 7 * mm
        box_h = 12 * mm
        col_split = PAGE_W * 0.68

        # Barra roja LINEA DE ABASTECIMIENTO
        c.setFillColor(RED)
        c.rect(MARGIN, top - bar_h, col_split - MARGIN - 2 * mm, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(MARGIN + 2 * mm, top - bar_h + 2.2 * mm, "L\u00cdNEA DE ABASTECIMIENTO:")

        # Barra roja LIDER
        c.setFillColor(RED)
        c.rect(col_split, top - bar_h, PAGE_W - MARGIN - col_split, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.drawString(col_split + 2 * mm, top - bar_h + 2.2 * mm, "L\u00cdDER:")

        # Caja blanca linea de abastecimiento
        box_top = top - bar_h
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(MARGIN, box_top - box_h, col_split - MARGIN - 2 * mm, box_h, fill=1, stroke=1)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 2 * mm, box_top - box_h + 4 * mm, self.familia.linea_abastecimiento or "")
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(MARGIN + 2 * mm, box_top - box_h + 8 * mm, "Descripci\u00f3n de familia:")

        # Caja blanca lider
        c.setFillColor(WHITE)
        c.rect(col_split, box_top - box_h, PAGE_W - MARGIN - col_split, box_h, fill=1, stroke=1)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica", 9)
        c.drawString(col_split + 2 * mm, box_top - box_h + 5 * mm, self.familia.lider or "")

        self.grid_top = box_top - box_h - 4 * mm

    def _section(self, x: float, y_top: float, w: float, h: float, title: str, lines: list[str]):
        """Dibuja un bloque: barra roja con titulo + caja blanca con lineas de texto."""
        c = self.c
        bar_h = 6 * mm
        c.setFillColor(RED)
        c.rect(x, y_top - bar_h, w, bar_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 2 * mm, y_top - bar_h + 1.8 * mm, title)

        box_h = h - bar_h
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.rect(x, y_top - h, w, box_h, fill=1, stroke=1)

        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica", 7.5)
        text_y = y_top - bar_h - 4 * mm
        line_h = 3.6 * mm
        max_lines = int(box_h / line_h) - 1
        rendered = 0
        for line in lines:
            wrapped = _wrap_text(c, line, "Helvetica", 7.5, w - 4 * mm)
            for wl in wrapped:
                if rendered >= max_lines:
                    break
                c.drawString(x + 2 * mm, text_y, wl)
                text_y -= line_h
                rendered += 1
            if rendered >= max_lines:
                break
        return y_top - h

    def _draw_grid(self):
        f = self.familia
        top = self.grid_top
        bottom = MARGIN
        total_h = top - bottom
        gap = 3 * mm

        col_w = (PAGE_W - 2 * MARGIN - 2 * gap) / 3
        x1 = MARGIN
        x2 = MARGIN + col_w + gap
        x3 = MARGIN + 2 * (col_w + gap)

        # columna izquierda: STATUS / CLASIFICACION PROVEEDORES / CLASIFICACION CLIENTE INTERNO
        h_left = [total_h * 0.28, total_h * 0.34, total_h * 0.38]
        status = f.status or {}
        status_lines = [
            f"Spend 2025: $ {status.get('spend_2025', 0)}",
            f"# Proveedores: {status.get('num_proveedores', 0)}",
            f"Spend bajo control: {status.get('spend_under_control', 0)}",
            f"# Proveedores SUC: {status.get('num_proveedores_suc', 0)}",
        ]
        y = self._section(x1, top, col_w, h_left[0], "STATUS", status_lines)

        cp = f.clasificacion_proveedores or {}
        cp_lines = [
            "Estrat\u00e9gicos: " + ", ".join(cp.get("estrategicos", []) or []),
            "Clave: " + ", ".join(cp.get("clave", []) or []),
            "T\u00e1cticos: " + ", ".join(cp.get("tacticos", []) or []),
        ]
        y = self._section(x1, y - gap, col_w, h_left[1], "CLASIFICACI\u00d3N PROVEEDORES", cp_lines)

        cci = f.clasificacion_cliente_interno or {}
        cci_lines = []
        for label, key in (("Estrat\u00e9gicos", "estrategicos"), ("Clave", "clave"), ("T\u00e1cticos", "tacticos")):
            item = cci.get(key, {}) or {}
            cci_lines.append(f"{label} - Spend: {item.get('spend', 0)} | # OCs: {item.get('ocs', 0)}")
        self._section(x1, y - gap, col_w, h_left[2], "CLASIFICACI\u00d3N CLIENTE INTERNO", cci_lines)

        # columna central: ANALISIS / KRALJIC / ACTORES PRINCIPALES / SUBFAMILIAS
        h_mid = [total_h * 0.30, total_h * 0.14, total_h * 0.28, total_h * 0.28]
        y = self._section(x2, top, col_w, h_mid[0], "AN\u00c1LISIS", [f.analisis_dofa or "Sin informaci\u00f3n."])
        kraljic_label = f.kraljic.value.replace("_", " ").title() if f.kraljic else "Sin definir"
        y = self._section(x2, y - gap, col_w, h_mid[1], "KRALJIC", [f"Cuadrante: {kraljic_label}"])
        y = self._section(
            x2, y - gap, col_w, h_mid[2], "ACTORES PRINCIPALES", [f.actores_principales or "Sin informaci\u00f3n."]
        )
        self._section(x2, y - gap, col_w, h_mid[3], "SUBFAMILIAS", [f.subfamilias or "Sin informaci\u00f3n."])

        # columna derecha: FACTORES RELEVANTES / PREMISAS DE NEGOCIACION / ESTRATEGIA A APLICAR
        h_right = [total_h * 0.24, total_h * 0.44, total_h * 0.32]
        y = self._section(
            x3, top, col_w, h_right[0], "FACTORES RELEVANTES", [f.factores_relevantes or "Sin informaci\u00f3n."]
        )
        y = self._section(
            x3, y - gap, col_w, h_right[1], "PREMISAS DE NEGOCIACI\u00d3N", [f.premisas_negociacion or "Sin informaci\u00f3n."]
        )
        self._section(
            x3, y - gap, col_w, h_right[2], "ESTRATEGIA A APLICAR", [f.estrategia_aplicar or "Sin informaci\u00f3n."]
        )


def generate_familia_pdf(familia: Familia) -> bytes:
    return FichaPDFBuilder(familia).build()
