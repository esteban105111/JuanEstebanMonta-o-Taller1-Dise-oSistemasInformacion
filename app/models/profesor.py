from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Profesor(Base):
    __tablename__ = "profesores"
    __table_args__ = (
        UniqueConstraint("tipo_identificacion", "numero_identificacion", name="uq_profesor_identificacion"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo_identificacion: Mapped[str] = mapped_column(String(20), nullable=False)
    numero_identificacion: Mapped[str] = mapped_column(String(40), nullable=False)
    especialidad: Mapped[str] = mapped_column(String(120), nullable=False)

    cursos: Mapped[list["Curso"]] = relationship(back_populates="profesor")

