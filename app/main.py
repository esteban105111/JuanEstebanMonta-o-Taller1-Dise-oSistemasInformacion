from fastapi import FastAPI

from app.config.settings import get_settings
from app.controllers.curso_controller import router as curso_router
from app.controllers.estudiante_controller import router as estudiante_router
from app.controllers.profesor_controller import router as profesor_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API REST para gestionar estudiantes, profesores y cursos del proyecto NOTASYA.",
)


@app.get("/health", tags=["Salud"])
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


app.include_router(estudiante_router)
app.include_router(profesor_router)
app.include_router(curso_router)

