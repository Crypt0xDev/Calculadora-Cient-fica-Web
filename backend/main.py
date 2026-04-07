# =============================================================
# Archivo  : main.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Punto de entrada del servidor. Aquí se crea la
#            aplicación FastAPI, se registran las rutas (routers)
#            y se sirven los archivos del frontend (HTML/CSS/JS).
# =============================================================

from fastapi import FastAPI                      # Framework para crear la API
from fastapi.staticfiles import StaticFiles      # Permite servir archivos estáticos
from fastapi.responses import FileResponse       # Para devolver archivos como respuesta
from backend.routers.calculadora import router   # Router con los endpoints de la calculadora
import os                                        # Para manejar rutas del sistema de archivos

# Creamos la aplicación FastAPI con un título descriptivo
# Este título aparece en la documentación automática: http://localhost:8000/docs
app = FastAPI(title="Calculadora Científica API")

# Registramos el router de la calculadora con el prefijo /api
# Todos los endpoints de la calculadora quedarán bajo /api/calcular/...
app.include_router(router, prefix="/api")

# Construimos la ruta hacia la carpeta del frontend
# os.path.dirname(__file__) → carpeta donde está este archivo (backend/)
# ".." sube un nivel → carpeta raíz del proyecto
# "frontend" → la carpeta con index.html, css y js
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Montamos los archivos estáticos bajo la URL /static
# Ejemplo: /static/css/style.css sirve el archivo frontend/css/style.css
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# Ruta raíz: cuando el usuario entra a http://localhost:8000
# devolvemos el index.html que es la interfaz de la calculadora
@app.get("/")
def index():
    return FileResponse(os.path.join(frontend_path, "index.html"))
