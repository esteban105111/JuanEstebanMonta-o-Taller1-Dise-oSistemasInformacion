from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"), nullable=False, index=True)
    profesor_id: Mapped[int] = mapped_column(ForeignKey("profesores.id"), nullable=False, index=True)
    calificacion: Mapped[Decimal] = mapped_column(Numeric(3, 1), nullable=False)

    estudiante: Mapped["Estudiante"] = relationship(back_populates="cursos")
    profesor: Mapped["Profesor"] = relationship(back_populates="cursos")

