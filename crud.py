from sqlalchemy.orm import Session
from schemas import OfertaCreate
from fastapi import HTTPException
from decimal import Decimal
from models import Evaluacion, Oferta
import math
from sqlalchemy.orm import Session
from models import Oferta
from schemas import OfertaCreate


def crear_oferta(db: Session, oferta: OfertaCreate):
    nueva_oferta = Oferta(
        proveedor=oferta.proveedor,
        precio=oferta.precio,
        calidad=oferta.calidad,
        tiempo_entrega=oferta.tiempo_entrega
    )

    db.add(nueva_oferta)
    db.commit()
    db.refresh(nueva_oferta)

    # 📌 Evaluación automática después de crear la oferta
    calcular_puntaje(db, nueva_oferta.id, metodo="aditivo")

    return nueva_oferta


def calcular_puntaje(db: Session, id_oferta: int, metodo: str = "aditivo"):
    """Calcula el puntaje de una oferta según el método de evaluación seleccionado y lo guarda en la BD."""

    oferta = db.query(Oferta).filter(Oferta.id == id_oferta).first()
    if not oferta:
        return None

    # **📌 Pesos de los criterios**
    pesos = {
        "calidad": 0.5,
        "precio": 0.3,
        "tiempo_entrega": 0.2
    }

    # **📌 Asignar valores por defecto para evitar NoneType**
    if oferta.tiempo_entrega is None or oferta.tiempo_entrega <= 0:
        oferta.tiempo_entrega = 30
    if oferta.precio is None or oferta.precio <= 0:
        oferta.precio = 100
    if oferta.calidad is None or oferta.calidad <= 0:
        oferta.calidad = 50

    # **📌 Normalización de valores**
    calidad_norm = max(0, min(1, oferta.calidad / 100))
    precio_norm = max(0, min(1, (100 - oferta.precio) / 100))
    tiempo_norm = max(0, min(1, (30 - oferta.tiempo_entrega) / 30))

    # **📊 Evaluación según el método**
    if metodo == "aditivo":
        puntaje_total = (
            calidad_norm * pesos["calidad"] +
            precio_norm * pesos["precio"] +
            tiempo_norm * pesos["tiempo_entrega"]
        ) * 100
    elif metodo == "multiplicativo":
        puntaje_total = round(
            math.pow(oferta.calidad, pesos["calidad"]) *
            math.pow(1 / max(oferta.precio, 1), pesos["precio"]) *
            math.pow(1 / max(oferta.tiempo_entrega, 1), pesos["tiempo_entrega"]),
            4
        )
    elif metodo == "leontieff":
        puntaje_total = min(calidad_norm, precio_norm, tiempo_norm) * 100
    else:
        return {"error": "Método no válido"}

    # **📌 Verificar si ya existe una evaluación para esta oferta y método**
    evaluacion_existente = db.query(Evaluacion).filter(
        Evaluacion.id_oferta == id_oferta,
        Evaluacion.metodo == metodo
    ).first()

    if evaluacion_existente:
        evaluacion_existente.puntaje_total = puntaje_total  # ✅ Actualizar puntaje
    else:
        nueva_evaluacion = Evaluacion(
            id_oferta=id_oferta,
            puntaje_total=puntaje_total,
            estado="aprobado",
            metodo=metodo  # ✅ Guardamos el método en la BD
        )
        db.add(nueva_evaluacion)

    db.commit()
    return {
        "id_oferta": id_oferta,
        "puntaje_total": puntaje_total,
        "estado": "aprobado",
        "metodo": metodo  # ✅ Ahora la respuesta incluye el método
    }

def obtener_evaluaciones(db: Session):
    """Obtiene todas las evaluaciones almacenadas en la base de datos."""
    evaluaciones = (
        db.query(Evaluacion)
        .join(Oferta, Evaluacion.id_oferta == Oferta.id)
        .add_columns(Oferta.proveedor, Evaluacion.revisado_por)
        .all()
    )

    return [
        {
            "id": e.Evaluacion.id,
            "id_oferta": e.Evaluacion.id_oferta,
            "proveedor": e.proveedor,
            "puntaje_total": e.Evaluacion.puntaje_total,
            "estado": e.Evaluacion.estado,
            "metodo": e.Evaluacion.metodo,
            "usuario": e.Evaluacion.revisado_por
        }
        for e in evaluaciones
    ]

