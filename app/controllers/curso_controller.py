from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dtos.curso_dto import CursoCreateDTO, CursoResponseDTO, CursoUpdateDTO
from app.patterns.service_factory import ServiceFactory
from app.services.curso_service import CursoService

router = APIRouter(prefix="/cursos", tags=["Cursos"])


def get_curso_service(db: Session = Depends(get_db)) -> CursoService:
    return ServiceFactory.crear_curso_service(db)


@router.get("", response_model=list[CursoResponseDTO])
def obtener_todos_los_cursos(service: CursoService = Depends(get_curso_service)):
    return service.obtener_todos_los_cursos()


@router.get("/{curso_id}", response_model=CursoResponseDTO)
def obtener_curso_por_id(
    curso_id: int,
    service: CursoService = Depends(get_curso_service),
):
    return service.obtener_curso_por_id(curso_id)


@router.post("", response_model=CursoResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_curso(
    dto: CursoCreateDTO,
    service: CursoService = Depends(get_curso_service),
):
    return service.crear_curso(dto)


@router.put("/{curso_id}", response_model=CursoResponseDTO)
def actualizar_curso(
    curso_id: int,
    dto: CursoUpdateDTO,
    service: CursoService = Depends(get_curso_service),
):
    return service.actualizar_curso(curso_id, dto)

