# =============================================================
# Archivo  : schemas/operacion.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Define los modelos de datos (schemas) usando Pydantic.
#            Pydantic valida automáticamente que los datos recibidos
#            en la API tengan el tipo correcto antes de procesarlos.
# =============================================================

from pydantic import BaseModel  # Clase base para definir modelos de datos


# ------------------------------------------------------------------
# Modelos para la calculadora científica (expresiones completas)
# ------------------------------------------------------------------

class ExpressionRequest(BaseModel):
    """
    Modelo de ENTRADA para evaluar una expresión matemática.
    Ejemplo de JSON que recibe: { "expresion": "sin(30) + sqrt(16)" }
    """
    expresion: str  # La expresión matemática como texto


class ExpressionResponse(BaseModel):
    """
    Modelo de SALIDA tras evaluar una expresión.
    Ejemplo de JSON que devuelve: { "resultado": "4.5", "expresion": "sin(30)+sqrt(16)" }
    """
    resultado: str  # El resultado como texto (para manejar decimales exactos)
    expresion: str  # La expresión original que se evaluó


# ------------------------------------------------------------------
# Modelos para operaciones simples entre dos números (compatibilidad)
# ------------------------------------------------------------------

class OperacionRequest(BaseModel):
    """
    Modelo de ENTRADA para una operación básica entre dos números.
    Ejemplo: { "numero1": 10, "numero2": 5, "operacion": "dividir" }
    """
    numero1: float    # Primer número (acepta decimales)
    numero2: float    # Segundo número (acepta decimales)
    operacion: str    # Nombre de la operación: sumar, restar, multiplicar, dividir


class OperacionResponse(BaseModel):
    """
    Modelo de SALIDA para una operación básica.
    Ejemplo: { "resultado": 2.0, "operacion": "dividir" }
    """
    resultado: float  # El resultado numérico
    operacion: str    # La operación que se realizó
