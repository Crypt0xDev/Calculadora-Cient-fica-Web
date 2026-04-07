<div align="center">

# 🧮 Calculadora Científica Web

**Calculadora científica de escritorio estilo CASIO fx — construida con Python + FastAPI y desplegada en Vercel.**

<br/>

[![Demo en vivo](https://img.shields.io/badge/▶%20Demo%20en%20vivo-calculadora--casio.vercel.app-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://calculadora-casio.vercel.app/)

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?style=flat-square&logo=pydantic&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
&nbsp;
[![CI](https://github.com/Crypt0xDev/Calculadora-Cient-fica-Web/actions/workflows/ci.yml/badge.svg)](https://github.com/Crypt0xDev/Calculadora-Cient-fica-Web/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<br/>

[📁 Estructura](docs/ESTRUCTURA.md) &nbsp;·&nbsp;
[🤝 Contribuir](docs/CONTRIBUTING.md) &nbsp;·&nbsp;
[🔒 Seguridad](docs/SECURITY.md) &nbsp;·&nbsp;
[🐛 Reportar un bug](https://github.com/Crypt0xDev/Calculadora-Cient-fica-Web/issues/new)

</div>

---

## ¿Qué es?

Calculadora científica completa que corre en el navegador. El usuario escribe expresiones matemáticas en la interfaz y el backend en **Python + FastAPI** las evalúa de forma segura, devolviendo el resultado como JSON.

> Diseño visual replica la serie **CASIO fx**: franja naranja, pantalla LCD verde, botones con relieve 3D y distribución en 5 columnas. Incluye vista previa del resultado en tiempo real mientras se escribe.

---

## ✨ Funciones

<table>
<tr>
<td>

**Aritmética**
- Suma, resta, multiplicación, división
- Módulo `%`
- Cambio de signo `+/-`

**Potencias y raíces**
- `x²` `x^y` `x⁻¹`
- `√x` `10ˣ`

**Memoria**
- `M+` `M−` `MR` `MC`

</td>
<td>

**Trigonometría**
- `sin` `cos` `tan`
- `sin⁻¹` `cos⁻¹` `tan⁻¹`
- Modo **DEG** y **RAD**

**Logaritmos y exponencial**
- `log₁₀` `ln` `eˣ`

**Otras**
- `|x|` `n!` `π` `e` `Ans` `CE`

</td>
</tr>
</table>

---

## 🏗️ Arquitectura

```
Navegador
├── index.html  →  style.css   (interfaz CASIO fx)
└── app.js      →  fetch() POST /api/calcular/expresion
                        │
                        ▼  HTTP / JSON
               Servidor FastAPI
               ├── routers/calculadora.py   (endpoints)
               ├── schemas/operacion.py     (validación Pydantic)
               └── services/operaciones.py  (eval() seguro)
```

---

## 🚀 Inicio rápido

**1. Clonar e instalar**
```bash
git clone https://github.com/Crypt0xDev/Calculadora-Cient-fica-Web.git
cd Calculadora-Cient-fica-Web
python -m venv .venv
```

**2. Activar entorno virtual**
```bash
# PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat

# Git Bash
source .venv/Scripts/activate
```

**3. Instalar dependencias y ejecutar**
```bash
pip install -r backend/requirements.txt
python main.py
```

**4. Abrir en el navegador**
```
http://localhost:8000
```

> 📖 Documentación interactiva de la API: `http://localhost:8000/docs`

---

## 🔌 API REST

<details>
<summary><b>POST /api/calcular/expresion</b> — Evalúa una expresión científica completa</summary>

```jsonc
// Petición
{ "expresion": "sin(30) + sqrt(16)" }

// Respuesta 200 OK
{ "resultado": "4.5", "expresion": "sin(30) + sqrt(16)" }

// Respuesta 400 Bad Request
{ "detail": "Expresión contiene caracteres no permitidos" }
```
</details>

<details>
<summary><b>POST /api/calcular/</b> — Operación básica entre dos números</summary>

```jsonc
// Petición
{ "numero1": 10, "numero2": 3, "operacion": "dividir" }

// Respuesta 200 OK
{ "resultado": 3.3333333333333335, "operacion": "dividir" }
```

Operaciones válidas: `sumar` · `restar` · `multiplicar` · `dividir`
</details>

---

## 🔐 Seguridad del `eval()`

El `eval()` corre en un entorno completamente aislado con **4 capas de protección**:

| # | Capa | Qué hace |
|:---:|:---|:---|
| 1 | **Whitelist de funciones** | Solo `sin`, `cos`, `sqrt`, `factorial`, `log`... son accesibles. |
| 2 | **Regex de caracteres** | Rechaza todo lo que no sea un carácter matemático válido. |
| 3 | **Blacklist de palabras** | Bloquea `__`, `import`, `exec`, `os`, `sys`, `globals`... |
| 4 | **`__builtins__` = `{}`** | El entorno no tiene acceso a las funciones internas de Python. |

---

## 🧪 Tests

```bash
python -m pytest tests/ -v
```

18 tests que cubren aritmética, funciones científicas, seguridad del `eval()` y manejo de errores.

---

## ⚙️ Variables de entorno

Crea un archivo `.env` en la raíz (opcional):

```ini
HOST=127.0.0.1   # 0.0.0.0 en producción
PORT=8000
```

---

## 📦 Dependencias

| Librería | Versión |
|:---|:---:|
| `fastapi` | 0.135.3 |
| `uvicorn[standard]` | 0.44.0 |
| `pydantic` | 2.12.5 |
| `python-dotenv` | 1.2.2 |

---

## 📄 Licencia

Distribuido bajo la licencia [MIT](LICENSE). &copy; 2026 Alexis Noe Gonzales Perez.


