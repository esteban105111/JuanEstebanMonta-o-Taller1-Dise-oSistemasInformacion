from fastapi import HTTPException, status

from app.dtos.profesor_dto import ProfesorCreateDTO, ProfesorUpdateDTO
from app.models.profesor import Profesor
from app.repositories.profesor_repository import ProfesorRepository


class ProfesorService:
    def __init__(self, repository: ProfesorRepository):
        self.repository = repository

    def obtener_todos_los_profesores(self) -> list[Profesor]:
        return self.repository.obtener_todos()

    def obtener_profesor_por_tipo_y_numero_identificacion(
        self,
        tipo_identificacion: str,
        numero_identificacion: str,
    ) -> Profesor:
        profesor = self.repository.obtener_por_tipo_y_numero_identificacion(
            tipo_identificacion,
            numero_identificacion,
        )
        if profesor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return profesor

    def crear_profesor(self, dto: ProfesorCreateDTO) -> Profesor:
        existente = self.repository.obtener_por_tipo_y_numero_identificacion(
            dto.tipo_identificacion,
            dto.numero_identificacion,
        )
        if existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un profesor con esa identificacion")
        profesor = Profesor(**dto.model_dump())
        return self.repository.crear(profesor)

    def actualizar_profesor(self, profesor_id: int, dto: ProfesorUpdateDTO) -> Profesor:
        profesor = self.repository.obtener_por_id(profesor_id)
        if profesor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")

        datos = dto.model_dump(exclude_unset=True)
        tipo = datos.get("tipo_identificacion", profesor.tipo_identificacion)
        numero = datos.get("numero_identificacion", profesor.numero_identificacion)
        existente = self.repository.obtener_por_tipo_y_numero_identificacion(tipo, numero)
        if existente and existente.id != profesor_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Identificacion ya registrada")

        return self.repository.actualizar(profesor, datos)

