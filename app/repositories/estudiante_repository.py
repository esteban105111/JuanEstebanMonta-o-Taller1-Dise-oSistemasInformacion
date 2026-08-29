from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estudiante import Estudiante


class EstudianteRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self) -> list[Estudiante]:
        return list(self.db.scalars(select(Estudiante).order_by(Estudiante.id)).all())

    def obtener_por_id(self, estudiante_id: int) -> Estudiante | None:
        return self.db.get(Estudiante, estudiante_id)

    def obtener_por_correo(self, correo: str) -> Estudiante | None:
        stmt = select(Estudiante).where(Estudiante.correo == correo)
        return self.db.scalar(stmt)

    def crear(self, estudiante: Estudiante) -> Estudiante:
        self.db.add(estudiante)
        self.db.commit()
        self.db.refresh(estudiante)
        return estudiante

    def actualizar(self, estudiante: Estudiante, datos: dict) -> Estudiante:
        for campo, valor in datos.items():
            setattr(estudiante, campo, valor)
        self.db.commit()
        self.db.refresh(estudiante)
        return estudiante

