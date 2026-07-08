# Contribuir al proyecto

## Requisitos
- Python 3.11
- GROQ_API_KEY (obtener en console.groq.com)

## Setup local
1. Clonar el repositorio
2. Crear entorno virtual con Python 3.11
3. Instalar dependencias con pip install -r requirements.txt
4. Copiar .env.example a .env y agregar tu GROQ_API_KEY
5. Ejecutar python -m app.ingest
6. Ejecutar uvicorn app.main:app --port 8000
