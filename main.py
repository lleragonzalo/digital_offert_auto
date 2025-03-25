from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import calcular_puntaje, obtener_evaluaciones
from typing import List
from models import Oferta, Evaluacion
import logging

# 📌 Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    """Verifica que la API está funcionando."""
    return {"message": "API funcionando correctamente"}

@app.put("/evaluacion/manual/{id_oferta}")
def actualizar_evaluacion_manual(id_oferta: int, puntaje_manual: float, usuario: str, db: Session = Depends(get_db)):
    """
    Permite actualizar manualmente el puntaje de una evaluación.

    - `id_oferta` (int): ID de la oferta que se va a modificar.
    - `puntaje_manual` (float): Nuevo puntaje asignado manualmente.
    - `usuario` (str): Nombre del usuario que realiza la modificación.

    Retorna un mensaje de éxito si la evaluación se actualiza correctamente.
    """

    evaluacion = db.query(Evaluacion).filter(Evaluacion.id_oferta == id_oferta).first()

    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    # ✅ Actualizar la evaluación con el nuevo puntaje y registrar el usuario que lo modificó
    evaluacion.puntaje_total = puntaje_manual
    evaluacion.revisado_por = usuario
    db.commit()

    return {
        "message": "Evaluación actualizada manualmente",
        "id_oferta": id_oferta,
        "nuevo_puntaje": puntaje_manual,
        "revisado_por": usuario
    }


@app.post("/evaluacion/{id_oferta}")
def evaluar_oferta(id_oferta: int, metodo: str = "aditivo", db: Session = Depends(get_db)):
    """Evalúa una oferta según el método seleccionado: aditivo, multiplicativo o leontieff.
       Solo evalúa ofertas existentes.
    """
    if id_oferta <= 0:
        raise HTTPException(status_code=400, detail="El ID de la oferta debe ser mayor a 0")

    # 📌 Verificar si la oferta ya existe
    oferta = db.query(Oferta).filter(Oferta.id == id_oferta).first()

    if not oferta:
        raise HTTPException(status_code=404, detail=f"No se encontró la oferta con ID {id_oferta}")

    # 📌 Evaluar la oferta con el método seleccionado
    resultado = calcular_puntaje(db, id_oferta, metodo)

    if not resultado:
        raise HTTPException(status_code=500, detail="Error en la evaluación de la oferta")

    logger.info(f"✅ Evaluación exitosa para la oferta {id_oferta} con método {metodo}: {resultado}")
    return resultado

@app.get("/ofertas/")
def obtener_ofertas(db: Session = Depends(get_db)):
    """Obtiene todas las ofertas registradas en la base de datos."""
    ofertas = db.query(Oferta).all()

    if not ofertas:
        raise HTTPException(status_code=404, detail="No hay ofertas registradas")

    return ofertas

@app.get("/evaluaciones/")
def listar_evaluaciones(db: Session = Depends(get_db)):
    """Lista todas las evaluaciones registradas."""
    evaluaciones = obtener_evaluaciones(db)

    if not evaluaciones:
        raise HTTPException(status_code=404, detail="No hay evaluaciones registradas")

    logger.info(f"🔍 Evaluaciones obtenidas: {evaluaciones}")
    return evaluaciones

@app.get("/dashboard/")
def obtener_dashboard(db: Session = Depends(get_db)):
    """Obtiene los resultados de las evaluaciones para mostrarlos en el Dashboard."""
    evaluaciones = obtener_evaluaciones(db)

    if not evaluaciones:
        raise HTTPException(status_code=404, detail="No hay datos para el dashboard")

    logger.info(f"📊 Datos enviados al Dashboard: {evaluaciones}")
    return evaluaciones
