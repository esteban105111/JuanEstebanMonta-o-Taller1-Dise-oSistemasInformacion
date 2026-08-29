from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CursoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    estudiante_id: int = Field(..., gt=0)
    profesor_id: int = Field(..., gt=0)
    calificacion: Decimal = Field(..., ge=0, le=5, decimal_places=1)


class CursoUpdateDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    estudiante_id: int | None = Field(default=None, gt=0)
    profesor_id: int | None = Field(default=None, gt=0)
    calificacion: Decimal | None = Field(default=None, ge=0, le=5, decimal_places=1)


class CursoResponseDTO(BaseModel):
    id: int
    nombre: str
    estudiante_id: int
    profesor_id: int
    calificacion: Decimal

    model_config = ConfigDict(from_attributes=True)

