"""create notasya tables

Revision ID: 20260828_0001
Revises:
Create Date: 2026-08-28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260828_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "estudiantes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("telefono", sa.String(length=30), nullable=False),
        sa.Column("correo", sa.String(length=180), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("correo"),
    )
    op.create_index(op.f("ix_estudiantes_correo"), "estudiantes", ["correo"], unique=False)
    op.create_index(op.f("ix_estudiantes_id"), "estudiantes", ["id"], unique=False)

    op.create_table(
        "profesores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("tipo_identificacion", sa.String(length=20), nullable=False),
        sa.Column("numero_identificacion", sa.String(length=40), nullable=False),
        sa.Column("especialidad", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tipo_identificacion", "numero_identificacion", name="uq_profesor_identificacion"),
    )
    op.create_index(op.f("ix_profesores_id"), "profesores", ["id"], unique=False)

    op.create_table(
        "cursos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("estudiante_id", sa.Integer(), nullable=False),
        sa.Column("profesor_id", sa.Integer(), nullable=False),
        sa.Column("calificacion", sa.Numeric(precision=3, scale=1), nullable=False),
        sa.ForeignKeyConstraint(["estudiante_id"], ["estudiantes.id"]),
        sa.ForeignKeyConstraint(["profesor_id"], ["profesores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cursos_estudiante_id"), "cursos", ["estudiante_id"], unique=False)
    op.create_index(op.f("ix_cursos_id"), "cursos", ["id"], unique=False)
    op.create_index(op.f("ix_cursos_profesor_id"), "cursos", ["profesor_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cursos_profesor_id"), table_name="cursos")
    op.drop_index(op.f("ix_cursos_id"), table_name="cursos")
    op.drop_index(op.f("ix_cursos_estudiante_id"), table_name="cursos")
    op.drop_table("cursos")
    op.drop_index(op.f("ix_profesores_id"), table_name="profesores")
    op.drop_table("profesores")
    op.drop_index(op.f("ix_estudiantes_id"), table_name="estudiantes")
    op.drop_index(op.f("ix_estudiantes_correo"), table_name="estudiantes")
    op.drop_table("estudiantes")

