from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    telefono: Mapped[str] = mapped_column(String(30), nullable=False)
    correo: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)

    cursos: Mapped[list["Curso"]] = relationship(back_populates="estudiante")

