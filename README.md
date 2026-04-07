<div align="center">

# 🧮 Calculadora Científica Web

### Aplicación de calculadora científica estilo CASIO fx con backend en Python

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?style=flat-square&logo=pydantic&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)

</div>

---

## Descripción

Calculadora científica completa que funciona íntegramente en el navegador. El usuario escribe expresiones matemáticas en la interfaz gráfica y el backend (Python + FastAPI) las evalúa de forma **segura** devolviendo el resultado en JSON.

El diseño visual replica fielmente la serie **CASIO fx**: franja naranja superior, pantalla LCD con tono verde, botones con efecto 3D y distribución en 5 columnas. Soporta notación científica, memoria, ángulos en DEG/RAD y vista previa del resultado en tiempo real.

---

## Funciones disponibles

| Categoría | Operaciones disponibles |
|:---|:---|
| **Aritmética básica** | `+` `−` `×` `÷` `%` |
| **Potencias y raíces** | `x²` `x^y` `x⁻¹` `10ˣ` `√x` |
| **Trigonométricas** | `sin` `cos` `tan` — en **DEG** o **RAD** |
| **Trigonométricas inversas** | `sin⁻¹` `cos⁻¹` `tan⁻¹` |
| **Logaritmos** | `log₁₀` `ln` `eˣ` |
| **Otras funciones** | `|x|` `n!` `π` `e` `Ans` `+/-` `CE` |
| **Memoria** | `M+` `M−` `MR` `MC` |

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────┐
│                        NAVEGADOR                            │
│   index.html  ──►  style.css                                │
│        │                                                    │
│      app.js  ──── fetch() POST ──────────────────────────┐  │
└──────────────────────────────────────────────────────────┼──┘
                                                           │
                               HTTP / JSON                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVIDOR FastAPI                       │
│                                                             │
│  backend/main.py                                            │
│       │                                                     │
│       ├── /api/calcular/expresion ──► routers/calculadora   │
│       │                                      │              │
│       │                              schemas/operacion.py   │
│       │                              (validación Pydantic)  │
│       │                                      │              │
│       │                              services/operaciones   │
│       │                              (eval() seguro)        │
│       │                                      │              │
│       └── /static/** ──► frontend/            └── resultado │
└─────────────────────────────────────────────────────────────┘
```

---

## Instalación y puesta en marcha

### Requisitos previos

- Python **3.11** o superior
- `pip` actualizado

### 1. Clonar el repositorio y crear el entorno virtual

```bash
git clone <url-del-repositorio>
cd Calculadora

python -m venv .venv
```

### 2. Activar el entorno virtual

```bash
# Windows — PowerShell
.venv\Scripts\Activate.ps1

# Windows — CMD
.venv\Scripts\activate.bat

# Windows — Git Bash
source .venv/Scripts/activate
```

### 3. Instalar dependencias

```bash
pip install -r backend/requirements.txt
```

### 4. Ejecutar el servidor

```bash
python main.py
```

### 5. Abrir en el navegador

```
http://localhost:8000
```

> La documentación interactiva de la API está disponible en `http://localhost:8000/docs`

---

## Referencia de la API REST

### `POST /api/calcular/expresion`

Endpoint principal. Evalúa cualquier expresión matemática científica.

**Petición**
```json
{
  "expresion": "sin(30) + sqrt(16)"
}
```

**Respuesta exitosa** `200 OK`
```json
{
  "resultado": "4.5",
  "expresion": "sin(30) + sqrt(16)"
}
```

**Respuesta de error** `400 Bad Request`
```json
{
  "detail": "Expresión contiene caracteres no permitidos"
}
```

---

### `POST /api/calcular/`

Endpoint para operaciones básicas entre dos números.

**Petición**
```json
{
  "numero1": 10,
  "numero2": 3,
  "operacion": "dividir"
}
```

**Respuesta exitosa** `200 OK`
```json
{
  "resultado": 3.3333333333333335,
  "operacion": "dividir"
}
```

> Operaciones válidas: `sumar`, `restar`, `multiplicar`, `dividir`

---

## Seguridad del `eval()`

El backend evalúa expresiones con `eval()` dentro de un entorno completamente aislado mediante **cuatro capas de protección**:

| Capa | Mecanismo | Descripción |
|:---:|:---|:---|
| 1 | **Whitelist de funciones** | Solo `sin`, `cos`, `sqrt`, `factorial`, `log`, etc. están permitidas. Ninguna otra función de Python es accesible. |
| 2 | **Regex de caracteres** | Se rechaza cualquier expresión que contenga caracteres fuera del conjunto matemático permitido. |
| 3 | **Blacklist de palabras** | Se bloquean tokens peligrosos: `__`, `import`, `exec`, `eval`, `open`, `os`, `sys`, `globals`, etc. |
| 4 | **`__builtins__` deshabilitados** | El entorno de `eval()` no tiene acceso a las funciones internas de Python. |

---

## Dependencias

| Librería | Versión | Descripción |
|:---|:---:|:---|
| `fastapi` | 0.135.3 | Framework web asíncrono para construir la API REST |
| `uvicorn[standard]` | 0.44.0 | Servidor ASGI de alto rendimiento para ejecutar FastAPI |
| `pydantic` | 2.12.5 | Validación y serialización automática de datos |
| `python-dotenv` | 1.2.2 | Lectura de variables de entorno desde `.env` |
| `pytest` | ≥ 9.0.0 | Framework para ejecutar las pruebas unitarias |

---

## Pruebas

> Las pruebas unitarias aún no están implementadas. La carpeta `tests/` no existe en el repositorio.
> Para crear y ejecutar pruebas en el futuro:

```bash
mkdir tests
pytest tests/ -v
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto para configurar el servidor:

```ini
# .env
HOST=127.0.0.1
PORT=8000
```

Si el archivo no existe, el servidor usará los valores por defecto (`127.0.0.1:8000`).

---


