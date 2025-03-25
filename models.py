from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Oferta(Base):
    __tablename__ = "ofertas"

    id = Column(Integer, primary_key=True, index=True)
    proveedor = Column(String, index=True)
    precio = Column(Float, nullable=False)
    calidad = Column(Float, nullable=False)
    tiempo_entrega = Column(Integer, nullable=False)  # ✅ Agregado tiempo_entrega correctamente

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_oferta = Column(Integer, ForeignKey("ofertas.id"))
    puntaje_total = Column(Float, nullable=False)
    estado = Column(String, default="aprobado")
    metodo = Column(String, nullable=True)  # Método de evaluación
    revisado_por = Column(String, nullable=True)  # ✅ Usuario que revisó manualmente la evaluación