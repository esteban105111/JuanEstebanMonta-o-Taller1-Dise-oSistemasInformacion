from sqlalchemy.orm import Session

from app.repositories.curso_repository import CursoRepository
from app.repositories.estudiante_repository import EstudianteRepository
from app.repositories.profesor_repository import ProfesorRepository
from app.services.curso_service import CursoService
from app.services.estudiante_service import EstudianteService
from app.services.profesor_service import ProfesorService


class ServiceFactory:
    @staticmethod
    def crear_estudiante_service(db: Session) -> EstudianteService:
        return EstudianteService(EstudianteRepository(db))

    @staticmethod
    def crear_profesor_service(db: Session) -> ProfesorService:
        return ProfesorService(ProfesorRepository(db))

    @staticmethod
    def crear_curso_service(db: Session) -> CursoService:
        return CursoService(
            CursoRepository(db),
            EstudianteRepository(db),
            ProfesorRepository(db),
        )

