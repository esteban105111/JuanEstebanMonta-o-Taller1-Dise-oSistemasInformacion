from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dtos.estudiante_dto import EstudianteCreateDTO, EstudianteResponseDTO, EstudianteUpdateDTO
from app.patterns.service_factory import ServiceFactory
from app.services.estudiante_service import EstudianteService

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


def get_estudiante_service(db: Session = Depends(get_db)) -> EstudianteService:
    return ServiceFactory.crear_estudiante_service(db)


@router.get("", response_model=list[EstudianteResponseDTO])
def obtener_todos_los_estudiantes(service: EstudianteService = Depends(get_estudiante_service)):
    return service.obtener_todos_los_estudiantes()


@router.get("/{correo}", response_model=EstudianteResponseDTO)
def obtener_estudiante_por_correo(
    correo: str = Path(..., description="Correo del estudiante"),
    service: EstudianteService = Depends(get_estudiante_service),
):
    return service.obtener_estudiante_por_correo(correo)


@router.post("", response_model=EstudianteResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_estudiante(
    dto: EstudianteCreateDTO,
    service: EstudianteService = Depends(get_estudiante_service),
):
    return service.crear_estudiante(dto)


@router.put("/{estudiante_id}", response_model=EstudianteResponseDTO)
def actualizar_estudiante(
    estudiante_id: int,
    dto: EstudianteUpdateDTO,
    service: EstudianteService = Depends(get_estudiante_service),
):
    return service.actualizar_estudiante(estudiante_id, dto)

