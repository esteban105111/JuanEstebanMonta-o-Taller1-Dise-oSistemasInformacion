from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.curso import Curso


class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self) -> list[Curso]:
        return list(self.db.scalars(select(Curso).order_by(Curso.id)).all())

    def obtener_por_id(self, curso_id: int) -> Curso | None:
        return self.db.get(Curso, curso_id)

    def crear(self, curso: Curso) -> Curso:
        self.db.add(curso)
        self.db.commit()
        self.db.refresh(curso)
        return curso

    def actualizar(self, curso: Curso, datos: dict) -> Curso:
        for campo, valor in datos.items():
            setattr(curso, campo, valor)
        self.db.commit()
        self.db.refresh(curso)
        return curso

