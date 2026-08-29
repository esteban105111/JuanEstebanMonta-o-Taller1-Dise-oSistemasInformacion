from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EstudianteCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    telefono: str = Field(..., min_length=7, max_length=30, pattern=r"^[0-9+\-\s()]+$")
    correo: EmailStr


class EstudianteUpdateDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    telefono: str | None = Field(default=None, min_length=7, max_length=30, pattern=r"^[0-9+\-\s()]+$")
    correo: EmailStr | None = None


class EstudianteResponseDTO(BaseModel):
    id: int
    nombre: str
    telefono: str
    correo: EmailStr

    model_config = ConfigDict(from_attributes=True)

