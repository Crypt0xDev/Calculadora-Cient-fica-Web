# =============================================================
# Archivo  : servicios/operaciones.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Contiene toda la lógica matemática del proyecto.
#            La función principal es evaluar_expresion(), que recibe
#            un texto como "sin(30)+sqrt(16)" y devuelve el resultado
#            de forma SEGURA (sin ejecutar código malicioso).
# =============================================================

import math          # Librería estándar de Python con funciones matemáticas
import re            # Librería para expresiones regulares (patrones de texto)
from fastapi import HTTPException  # Para lanzar errores HTTP con mensaje descriptivo

# ------------------------------------------------------------------
# WHITELIST de funciones permitidas
# Solo estas funciones pueden usarse en las expresiones del usuario.
# Esto evita que alguien escriba código peligroso como "os.system()".
# ------------------------------------------------------------------
FUNCIONES_PERMITIDAS = {
    # Trigonométricas
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    # Hiperbólicas
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    # Logaritmos y exponencial
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "sqrt": math.sqrt,
    # Otras
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
    "factorial": math.factorial,
    # Constantes
    "pi": math.pi,
    "e": math.e,
}

# Patrón de seguridad: solo permite dígitos, letras, operadores y paréntesis
# Si la expresión tiene algo diferente (ej. comillas, punto y coma), se rechaza
_PATRON_SEGURO = re.compile(r'^[\d\s\.\+\-\*\/\^\(\)\,a-zA-Z_]+$')


def evaluar_expresion(expresion: str) -> str:
    """
    Evalúa una expresión matemática completa de forma segura.
    Pasos:
      1. Validar que no esté vacía
      2. Verificar que solo tenga caracteres matemáticos
      3. Bloquear palabras peligrosas de Python
      4. Convertir símbolos (^ → **)
      5. Evaluar en un entorno aislado (sin acceso a módulos del sistema)
      6. Formatear y devolver el resultado
    """
    # Paso 1: verificar que la expresión no esté vacía
    if not expresion or not expresion.strip():
        raise HTTPException(status_code=400, detail="Expresión vacía")

    # Paso 2: validar que solo tenga caracteres matemáticos válidos
    if not _PATRON_SEGURO.match(expresion):
        raise HTTPException(status_code=400, detail="Expresión contiene caracteres no permitidos")

    # Paso 3: bloquear palabras que podrían ejecutar código peligroso
    # Ejemplo: alguien podría escribir "__import__('os').system('rm -rf /')"
    # Usamos lookbehind/lookahead para palabras alfabéticas, evitando falsos
    # positivos como "os" dentro de "cos" o "acos".
    palabras_prohibidas = [
        "__", "import", "exec", "eval", "open", "os", "sys",
        "compile", "globals", "locals", "getattr", "setattr",
        "delattr", "vars", "dir", "type", "input", "print",
    ]
    expr_lower = expresion.lower()
    for palabra in palabras_prohibidas:
        if palabra.replace("_", "").isalpha():
            # Búsqueda de palabra completa: "os" no debe coincidir dentro de "cos"
            if re.search(r'(?<![a-zA-Z])' + re.escape(palabra) + r'(?![a-zA-Z])', expr_lower):
                raise HTTPException(status_code=400, detail="Expresión no permitida")
        else:
            # Subcadena exacta para tokens especiales como "__"
            if palabra in expr_lower:
                raise HTTPException(status_code=400, detail="Expresión no permitida")

    # Paso 4a: convertir ^ (potencia matemática) a ** (potencia en Python)
    expresion = expresion.replace('^', '**')

    # Paso 4b: convertir funciones en grados (sind, cosd, tand) a radianes
    # El frontend manda "sind(30)" cuando el modo es DEG, y aquí lo convertimos
    # Ejemplo: sind(30) → sin(math.radians(30))
    expresion = re.sub(
        r'\b(sin|cos|tan)d\(([^)]+)\)',
        lambda m: f"{m.group(1)}(math.radians({m.group(2)}))",
        expresion
    )

    try:
        # Paso 5: evaluar la expresión en un entorno AISLADO
        # __builtins__: {} elimina todas las funciones built-in de Python
        # Solo dejamos math y nuestra whitelist de funciones
        entorno = {"__builtins__": {}, "math": math}
        entorno.update(FUNCIONES_PERMITIDAS)
        resultado = eval(expresion, entorno)  # noqa: S307

        # Validaciones del resultado obtenido
        if isinstance(resultado, complex):
            raise HTTPException(status_code=400, detail="Resultado complejo no soportado")
        if not isinstance(resultado, (int, float)):
            raise HTTPException(status_code=400, detail="El resultado no es un número")
        if math.isinf(resultado):   # Ej: 1/0 en modo float da infinito
            raise HTTPException(status_code=400, detail="Resultado infinito")
        if math.isnan(resultado):   # Ej: 0/0 → NaN (Not a Number)
            raise HTTPException(status_code=400, detail="Resultado indefinido")

        # Paso 6: formatear el resultado
        # Si es un número entero (ej: 120.0), devolver sin decimales → "120"
        if isinstance(resultado, (int, float)) and resultado == int(resultado):
            return str(int(resultado))
        # Si tiene decimales, limitar a 10 cifras y quitar ceros al final
        # Ejemplo: 0.3333333333000 → "0.3333333333"
        formatted = f"{resultado:.10f}".rstrip('0').rstrip('.')
        return formatted

    except HTTPException:
        raise  # Re-lanzar errores HTTP que nosotros mismos generamos
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="División entre cero")
    except ValueError as e:
        # Ejemplo: sqrt(-1) lanza ValueError en Python
        raise HTTPException(status_code=400, detail=f"Error matemático: {str(e)}")
    except Exception:
        raise HTTPException(status_code=400, detail="Expresión inválida")


# ------------------------------------------------------------------
# Operaciones simples entre dos números (se mantienen por compatibilidad)
# ------------------------------------------------------------------

def sumar(a: float, b: float) -> float:
    return a + b          # Suma básica

def restar(a: float, b: float) -> float:
    return a - b          # Resta básica

def multiplicar(a: float, b: float) -> float:
    return a * b          # Multiplicación

def dividir(a: float, b: float) -> float:
    if b == 0:            # Protección contra división entre cero
        raise HTTPException(status_code=400, detail="No se puede dividir entre cero")
    return a / b

# Diccionario que mapea el nombre de la operación a su función
# Ventaja: evita usar if/elif para cada operación
OPERACIONES = {"sumar": sumar, "restar": restar, "multiplicar": multiplicar, "dividir": dividir}

def calcular(numero1: float, numero2: float, operacion: str) -> float:
    """
    Ejecuta una operación básica buscando en el diccionario OPERACIONES.
    Lanza HTTP 400 si la operación no existe, en vez de un keyerror 500.
    """
    if operacion not in OPERACIONES:
        raise HTTPException(
            status_code=400,
            detail=f"Operación '{operacion}' no reconocida. "
                   f"Opciones: {list(OPERACIONES.keys())}"
        )
    return OPERACIONES[operacion](numero1, numero2)
