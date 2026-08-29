from fastapi import HTTPException, status

from app.dtos.curso_dto import CursoCreateDTO, CursoUpdateDTO
from app.models.curso import Curso
from app.repositories.curso_repository import CursoRepository
from app.repositories.estudiante_repository import EstudianteRepository
from app.repositories.profesor_repository import ProfesorRepository


class CursoService:
    def __init__(
        self,
        curso_repository: CursoRepository,
        estudiante_repository: EstudianteRepository,
        profesor_repository: ProfesorRepository,
    ):
        self.curso_repository = curso_repository
        self.estudiante_repository = estudiante_repository
        self.profesor_repository = profesor_repository

    def obtener_todos_los_cursos(self) -> list[Curso]:
        return self.curso_repository.obtener_todos()

    def obtener_curso_por_id(self, curso_id: int) -> Curso:
        curso = self.curso_repository.obtener_por_id(curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        return curso

    def crear_curso(self, dto: CursoCreateDTO) -> Curso:
        self._validar_relaciones(dto.estudiante_id, dto.profesor_id)
        curso = Curso(**dto.model_dump())
        return self.curso_repository.crear(curso)

    def actualizar_curso(self, curso_id: int, dto: CursoUpdateDTO) -> Curso:
        curso = self.curso_repository.obtener_por_id(curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")

        datos = dto.model_dump(exclude_unset=True)
        estudiante_id = datos.get("estudiante_id", curso.estudiante_id)
        profesor_id = datos.get("profesor_id", curso.profesor_id)
        self._validar_relaciones(estudiante_id, profesor_id)
        return self.curso_repository.actualizar(curso, datos)

    def _validar_relaciones(self, estudiante_id: int, profesor_id: int) -> None:
        if self.estudiante_repository.obtener_por_id(estudiante_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no existe")
        if self.profesor_repository.obtener_por_id(profesor_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no existe")

