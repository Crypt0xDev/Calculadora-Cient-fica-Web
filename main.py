# =============================================================
# Archivo  : main.py
# Autor    : Alexis Noe Gonzales Perez
# Proyecto : Calculadora Científica Web
# Desc.    : Punto de entrada del proyecto. Ejecuta el servidor
#            FastAPI con Uvicorn. HOST y PORT se leen desde el
#            archivo .env (local) o variables de entorno (Vercel).
#            Para iniciar en local: python main.py
# =============================================================

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        reload=False,
    )
