from pydantic import condecimal, conint
from pydantic import BaseModel

class OfertaCreate(BaseModel):
    proveedor: str
    precio: condecimal(gt=0, decimal_places=2)  # Mayor a 0, con 2 decimales
    calidad: conint(ge=0, le=100)  # Entre 0 y 100


class EvaluacionResponse(BaseModel):
    id: int
    id_oferta: int
    puntaje_total: float
    estado: str















