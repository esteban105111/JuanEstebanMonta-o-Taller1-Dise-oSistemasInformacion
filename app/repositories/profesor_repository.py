from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profesor import Profesor


class ProfesorRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self) -> list[Profesor]:
        return list(self.db.scalars(select(Profesor).order_by(Profesor.id)).all())

    def obtener_por_id(self, profesor_id: int) -> Profesor | None:
        return self.db.get(Profesor, profesor_id)

    def obtener_por_tipo_y_numero_identificacion(
        self,
        tipo_identificacion: str,
        numero_identificacion: str,
    ) -> Profesor | None:
        stmt = select(Profesor).where(
            Profesor.tipo_identificacion == tipo_identificacion,
            Profesor.numero_identificacion == numero_identificacion,
        )
        return self.db.scalar(stmt)

    def crear(self, profesor: Profesor) -> Profesor:
        self.db.add(profesor)
        self.db.commit()
        self.db.refresh(profesor)
        return profesor

    def actualizar(self, profesor: Profesor, datos: dict) -> Profesor:
        for campo, valor in datos.items():
            setattr(profesor, campo, valor)
        self.db.commit()
        self.db.refresh(profesor)
        return profesor

