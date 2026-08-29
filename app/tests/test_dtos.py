from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.dtos.curso_dto import CursoCreateDTO
from app.dtos.estudiante_dto import EstudianteCreateDTO


def test_estudiante_create_dto_valido():
    dto = EstudianteCreateDTO(nombre="Ana Perez", telefono="3001234567", correo="ana@test.com")

    assert dto.correo == "ana@test.com"


def test_estudiante_create_dto_rechaza_correo_invalido():
    with pytest.raises(ValidationError):
        EstudianteCreateDTO(nombre="Ana Perez", telefono="3001234567", correo="correo-invalido")


def test_curso_create_dto_rechaza_calificacion_fuera_de_rango():
    with pytest.raises(ValidationError):
        CursoCreateDTO(nombre="Matematicas", estudiante_id=1, profesor_id=1, calificacion=Decimal("5.5"))

