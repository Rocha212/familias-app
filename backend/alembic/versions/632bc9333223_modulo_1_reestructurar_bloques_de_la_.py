"""modulo 1: reestructurar bloques de la ficha (pagina 1)

Revision ID: 632bc9333223
Revises: 819fa8509b1e
Create Date: 2026-07-15 20:35:13.853765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '632bc9333223'
down_revision: Union[str, None] = '819fa8509b1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Defaults usados para rellenar filas ya existentes al agregar/reestructurar columnas.
ANALISIS_INTERNO_DEFAULT_JSON = (
    '{"spend": {"y_menos_1": 0, "y": 0, "y_mas_1": 0}, '
    '"pct_cobertura": {"y_menos_1": 0, "y": 0, "y_mas_1": 0}, '
    '"spend_under_control": {"y_menos_1": 0, "y": 0, "y_mas_1": 0}}'
)
PODER_NEGOCIACION_DEFAULT_JSON = '{"veolia": null, "proveedor": null}'
DOFA_DEFAULT_JSON = (
    '{"debilidades": "", "fortalezas": "", "oportunidades": "", "amenazas": ""}'
)
FACTORES_RELEVANTES_DEFAULT_JSON = (
    '{"insights": "", "indicadores_economicos_financieros": ""}'
)


def upgrade() -> None:
    # --- Columnas nuevas: se agregan nullable, se rellenan, luego se fijan NOT NULL ---
    op.add_column('familias', sa.Column('analisis_interno', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('familias', sa.Column('poder_negociacion', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    op.execute(f"UPDATE familias SET analisis_interno = '{ANALISIS_INTERNO_DEFAULT_JSON}'::jsonb WHERE analisis_interno IS NULL")
    op.execute(f"UPDATE familias SET poder_negociacion = '{PODER_NEGOCIACION_DEFAULT_JSON}'::jsonb WHERE poder_negociacion IS NULL")

    op.alter_column('familias', 'analisis_interno', nullable=False)
    op.alter_column('familias', 'poder_negociacion', nullable=False)

    # --- analisis_dofa: de TEXT libre a JSONB estructurado. No hay mapeo automatico
    #     valido desde texto libre, asi que se reemplaza el contenido (no hay datos
    #     reales que preservar en este momento del proyecto). ---
    op.drop_column('familias', 'analisis_dofa')
    op.add_column(
        'familias',
        sa.Column(
            'analisis_dofa',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text(f"'{DOFA_DEFAULT_JSON}'::jsonb"),
        ),
    )
    op.alter_column('familias', 'analisis_dofa', server_default=None)

    # --- factores_relevantes: mismo caso que analisis_dofa ---
    op.drop_column('familias', 'factores_relevantes')
    op.add_column(
        'familias',
        sa.Column(
            'factores_relevantes',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text(f"'{FACTORES_RELEVANTES_DEFAULT_JSON}'::jsonb"),
        ),
    )
    op.alter_column('familias', 'factores_relevantes', server_default=None)


def downgrade() -> None:
    op.drop_column('familias', 'factores_relevantes')
    op.add_column('familias', sa.Column('factores_relevantes', sa.TEXT(), nullable=False, server_default=""))
    op.alter_column('familias', 'factores_relevantes', server_default=None)

    op.drop_column('familias', 'analisis_dofa')
    op.add_column('familias', sa.Column('analisis_dofa', sa.TEXT(), nullable=False, server_default=""))
    op.alter_column('familias', 'analisis_dofa', server_default=None)

    op.drop_column('familias', 'poder_negociacion')
    op.drop_column('familias', 'analisis_interno')