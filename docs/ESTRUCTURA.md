# Estructura del Proyecto — Calculadora Científica Web

## Árbol de archivos

```
Calculadora/
│
├── main.py                   ← Punto de entrada: python main.py
├── .env                      ← Variables de entorno: HOST y PORT
├── .gitignore
├── README.md                 ← Documentación principal del proyecto
├── ESTRUCTURA.md             ← Este archivo
│
├── backend/                  ← Servidor: lógica, validación y rutas
│   ├── main.py               ← Crea la app FastAPI y monta el frontend
│   ├── requirements.txt      ← Dependencias Python del proyecto
│   │
│   ├── routers/
│   │   └── calculadora.py    ← Endpoints REST de la calculadora
│   │
│   ├── schemas/
│   │   └── operacion.py      ← Modelos Pydantic para validar datos
│   │
│   └── services/
│       └── operaciones.py    ← Lógica matemática y eval() seguro
│
├── frontend/                 ← Cliente: todo lo que ve el usuario
│   ├── index.html            ← Interfaz CASIO fx (HTML5)
│   ├── css/
│   │   └── style.css         ← Diseño: LCD verde, gris carbón
│   └── js/
│       └── app.js            ← Lógica de botones y llamadas a la API
│
└── .venv/                    ← Entorno virtual Python (no se sube a Git)
```

---

## Responsabilidad de cada capa

### Raíz del proyecto

| Archivo | Propósito |
|:---|:---|
| `main.py` | Lanza el servidor Uvicorn. Lee `HOST` y `PORT` desde `.env`. |
| `.env` | Configura `HOST` y `PORT`. No se incluye en el repositorio (ver `.gitignore`). |
| `.gitignore` | Excluye `.venv/`, `.env`, `__pycache__/` y `.pytest_cache/` del control de versiones. |

---

### `backend/` — Servidor

| Archivo | Responsabilidad |
|:---|:---|
| `main.py` | Inicializa FastAPI, registra routers y sirve el frontend como archivos estáticos bajo `/static`. |
| `requirements.txt` | Lista de dependencias Python: FastAPI, Uvicorn, Pydantic, python-dotenv. |

#### `routers/calculadora.py`
Define los dos endpoints de la API:
- `POST /api/calcular/` → operación simple entre dos números.
- `POST /api/calcular/expresion` → evalúa una expresión científica completa.

#### `schemas/operacion.py`
Modelos Pydantic que validan automáticamente los datos antes de que lleguen a la lógica:
- `ExpressionRequest` / `ExpressionResponse` — para expresiones científicas.
- `OperacionRequest` / `OperacionResponse` — para operaciones numéricas básicas.

#### `services/operaciones.py`
Contiene la lógica matemática central:
- `evaluar_expresion()` — evalúa expresiones con `eval()` en un entorno aislado (whitelist + regex + blacklist).
- `calcular()` — ejecuta operaciones básicas (sumar, restar, multiplicar, dividir).

---

### `frontend/` — Cliente

| Archivo | Responsabilidad |
|:---|:---|
| `index.html` | Estructura HTML de la calculadora. Diseño CASIO fx con 5 columnas de botones. |
| `css/style.css` | Estilos visuales: franja naranja, pantalla LCD verde, botones 3D, tipografía monoespaciada. |
| `js/app.js` | Maneja eventos de botones, construye la expresión, llama a la API con `fetch()` y muestra el resultado. |

---

## Flujo de datos

```
[Usuario presiona botón]
        │
        ▼
  app.js construye la expresión
        │
        ▼
  fetch() → POST /api/calcular/expresion
        │
        ▼
  routers/calculadora.py  recibe la petición
        │
        ▼
  schemas/operacion.py    valida el JSON (Pydantic)
        │
        ▼
  services/operaciones.py evalúa de forma segura
        │
        ▼
  Respuesta JSON  →  app.js muestra el resultado
```

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|:---|:---|:---:|
| Servidor web | FastAPI + Uvicorn | 0.135 / 0.44 |
| Validación de datos | Pydantic | 2.x |
| Lenguaje backend | Python | 3.11+ |
| Interfaz de usuario | HTML5 + CSS3 | — |
| Lógica del cliente | JavaScript | ES6+ |
