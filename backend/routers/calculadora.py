# =============================================================
# Archivo  : routers/calculadora.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Define los endpoints (rutas) de la API REST.
#            Un endpoint es una URL a la que el frontend envía
#            datos y recibe una respuesta en formato JSON.
# =============================================================

from fastapi import APIRouter  # Permite agrupar rutas relacionadas
from backend.schemas.operacion import (
    OperacionRequest, OperacionResponse,    # Schemas para operaciones básicas
    ExpressionRequest, ExpressionResponse,  # Schemas para expresiones completas
)
from backend.services.operaciones import calcular, evaluar_expresion  # Lógica matemática

# Creamos el router con prefijo /calcular
# Como en main.py ya tiene /api, las rutas completas serán:
#   - POST /api/calcular/          → operación simple (dos números)
#   - POST /api/calcular/expresion → expresión científica completa
router = APIRouter(prefix="/calcular", tags=["Calculadora"])


@router.post("/", response_model=OperacionResponse)
def realizar_operacion(datos: OperacionRequest):
    """
    Endpoint para operaciones simples entre dos números.
    Recibe: { numero1, numero2, operacion }
    Devuelve: { resultado, operacion }
    """
    # Llamamos al servicio que ejecuta la operación matemática
    resultado = calcular(datos.numero1, datos.numero2, datos.operacion)
    # Devolvemos el resultado empaquetado en el schema de respuesta
    return OperacionResponse(resultado=resultado, operacion=datos.operacion)


@router.post("/expresion", response_model=ExpressionResponse)
def evaluar(datos: ExpressionRequest):
    """
    Endpoint principal de la calculadora científica.
    Recibe una expresión completa como texto: { "expresion": "sin(30)+2^8" }
    Devuelve el resultado: { "resultado": "256.5", "expresion": "sin(30)+2^8" }
    """
    # Mandamos la expresión al servicio que la evalúa de forma segura
    resultado = evaluar_expresion(datos.expresion)
    return ExpressionResponse(resultado=resultado, expresion=datos.expresion)

