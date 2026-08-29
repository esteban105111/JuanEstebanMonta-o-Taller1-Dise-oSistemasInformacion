from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.dtos.curso_dto import CursoCreateDTO
from app.dtos.estudiante_dto import EstudianteCreateDTO
from app.services.curso_service import CursoService
from app.services.estudiante_service import EstudianteService


class FakeEstudianteRepository:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def obtener_todos(self):
        return list(self.items.values())

    def obtener_por_id(self, estudiante_id):
        return self.items.get(estudiante_id)

    def obtener_por_correo(self, correo):
        return next((item for item in self.items.values() if item.correo == correo), None)

    def crear(self, estudiante):
        estudiante.id = self.next_id
        self.items[self.next_id] = estudiante
        self.next_id += 1
        return estudiante

    def actualizar(self, estudiante, datos):
        for key, value in datos.items():
            setattr(estudiante, key, value)
        return estudiante


class FakeProfesorRepository:
    def __init__(self, existe=True):
        self.existe = existe

    def obtener_por_id(self, profesor_id):
        if self.existe:
            return SimpleNamespace(id=profesor_id)
        return None


class FakeCursoRepository:
    def __init__(self):
        self.items = {}

    def obtener_todos(self):
        return list(self.items.values())

    def obtener_por_id(self, curso_id):
        return self.items.get(curso_id)

    def crear(self, curso):
        curso.id = 1
        self.items[1] = curso
        return curso

    def actualizar(self, curso, datos):
        for key, value in datos.items():
            setattr(curso, key, value)
        return curso


def test_crear_estudiante_rechaza_correo_duplicado():
    repo = FakeEstudianteRepository()
    service = EstudianteService(repo)
    dto = EstudianteCreateDTO(nombre="Ana Perez", telefono="3001234567", correo="ana@test.com")
    service.crear_estudiante(dto)

    with pytest.raises(HTTPException) as exc:
        service.crear_estudiante(dto)

    assert exc.value.status_code == 409


def test_crear_curso_rechaza_estudiante_inexistente():
    service = CursoService(FakeCursoRepository(), FakeEstudianteRepository(), FakeProfesorRepository())
    dto = CursoCreateDTO(nombre="Bases de Datos", estudiante_id=99, profesor_id=1, calificacion=Decimal("4.2"))

    with pytest.raises(HTTPException) as exc:
        service.crear_curso(dto)

    assert exc.value.status_code == 404

