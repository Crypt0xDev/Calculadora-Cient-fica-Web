# =============================================================
# Archivo  : _main.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Punto de entrada del proyecto. Ejecuta el servidor
#            FastAPI con Uvicorn. HOST y PORT se leen desde el
#            archivo .env para no tener datos hardcodeados.
#            Para iniciar: python _main.py
# =============================================================

import uvicorn
import os
from dotenv import load_dotenv  # Lee las variables del archivo .env

# Carga las variables definidas en .env al entorno del proceso
load_dotenv()

# Leer HOST y PORT desde .env; si no existen, usar valores por defecto
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )
