from pydantic import BaseModel, ConfigDict, Field


class ProfesorCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo_identificacion: str = Field(..., min_length=2, max_length=20)
    numero_identificacion: str = Field(..., min_length=4, max_length=40)
    especialidad: str = Field(..., min_length=2, max_length=120)


class ProfesorUpdateDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    tipo_identificacion: str | None = Field(default=None, min_length=2, max_length=20)
    numero_identificacion: str | None = Field(default=None, min_length=4, max_length=40)
    especialidad: str | None = Field(default=None, min_length=2, max_length=120)


class ProfesorResponseDTO(BaseModel):
    id: int
    nombre: str
    tipo_identificacion: str
    numero_identificacion: str
    especialidad: str

    model_config = ConfigDict(from_attributes=True)

