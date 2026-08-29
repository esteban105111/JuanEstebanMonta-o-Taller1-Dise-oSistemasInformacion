from fastapi import HTTPException, status

from app.dtos.estudiante_dto import EstudianteCreateDTO, EstudianteUpdateDTO
from app.models.estudiante import Estudiante
from app.repositories.estudiante_repository import EstudianteRepository


class EstudianteService:
    def __init__(self, repository: EstudianteRepository):
        self.repository = repository

    def obtener_todos_los_estudiantes(self) -> list[Estudiante]:
        return self.repository.obtener_todos()

    def obtener_estudiante_por_correo(self, correo: str) -> Estudiante:
        estudiante = self.repository.obtener_por_correo(correo)
        if estudiante is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        return estudiante

    def crear_estudiante(self, dto: EstudianteCreateDTO) -> Estudiante:
        if self.repository.obtener_por_correo(str(dto.correo)):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un estudiante con ese correo")
        estudiante = Estudiante(**dto.model_dump())
        return self.repository.crear(estudiante)

    def actualizar_estudiante(self, estudiante_id: int, dto: EstudianteUpdateDTO) -> Estudiante:
        estudiante = self.repository.obtener_por_id(estudiante_id)
        if estudiante is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

        datos = dto.model_dump(exclude_unset=True)
        if "correo" in datos:
            existente = self.repository.obtener_por_correo(str(datos["correo"]))
            if existente and existente.id != estudiante_id:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Correo ya registrado")

        return self.repository.actualizar(estudiante, datos)

