from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dtos.profesor_dto import ProfesorCreateDTO, ProfesorResponseDTO, ProfesorUpdateDTO
from app.patterns.service_factory import ServiceFactory
from app.services.profesor_service import ProfesorService

router = APIRouter(prefix="/profesores", tags=["Profesores"])


def get_profesor_service(db: Session = Depends(get_db)) -> ProfesorService:
    return ServiceFactory.crear_profesor_service(db)


@router.get("", response_model=list[ProfesorResponseDTO])
def obtener_todos_los_profesores(service: ProfesorService = Depends(get_profesor_service)):
    return service.obtener_todos_los_profesores()


@router.get("/{tipo_identificacion}/{numero_identificacion}", response_model=ProfesorResponseDTO)
def obtener_profesor_por_tipo_y_numero_identificacion(
    tipo_identificacion: str = Path(..., description="Tipo de identificacion"),
    numero_identificacion: str = Path(..., description="Numero de identificacion"),
    service: ProfesorService = Depends(get_profesor_service),
):
    return service.obtener_profesor_por_tipo_y_numero_identificacion(tipo_identificacion, numero_identificacion)


@router.post("", response_model=ProfesorResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_profesor(
    dto: ProfesorCreateDTO,
    service: ProfesorService = Depends(get_profesor_service),
):
    return service.crear_profesor(dto)


@router.put("/{profesor_id}", response_model=ProfesorResponseDTO)
def actualizar_profesor(
    profesor_id: int,
    dto: ProfesorUpdateDTO,
    service: ProfesorService = Depends(get_profesor_service),
):
    return service.actualizar_profesor(profesor_id, dto)

