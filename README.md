# 🛍️ Agente RAG - BimBam Buy

Agente de IA que responde preguntas sobre documentos internos de BimBam Buy, construido con LangChain + Groq (Llama 3) para el Challenge Oracle ONE / Alura.

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| LLM | Llama 3.3 70B via Groq API |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Vector store | FAISS |
| Orquestación | LangChain 0.2 |
| API | FastAPI + Uvicorn |
| Documentos | 5 PDFs de BimBam Buy (57 páginas) |

## 🏗️ Arquitectura
Pregunta → FastAPI → FAISS retriever → Groq Llama 3 → Respuesta

## 📄 Documentos base

- Política de Reembolsos y Devoluciones
- Programa de Afiliados
- Guía de Tiempos y Costos de Envío
- Preguntas Frecuentes sobre Métodos de Pago
- Manual de Garantía de Productos

## 📁 Estructura del proyecto
alura-challenge-bimbambuy/

├── app/

│   ├── ingest.py   ← procesa PDFs y crea vector store

│   ├── agent.py    ← cadena RAG con LangChain + Groq

│   └── main.py     ← API FastAPI + interfaz de chat

├── data/pdfs/      ← documentos de BimBam Buy

├── docs/           ← capturas de pantalla

├── .env.example

└── requirements.txt

## ⚙️ Instalación

```bash
git clone https://github.com/Maddock12318/alura-challenge-bimbambuy.git
cd alura-challenge-bimbambuy
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Agregar GROQ_API_KEY en el archivo .env
python -m app.ingest
uvicorn app.main:app --port 8000
```

## 🚀 Uso

Abre `http://localhost:8000` en tu navegador para usar el chat.

O usa la API directamente:

```bash
POST http://localhost:8000/ask
{"question": "¿Cuál es la política de reembolsos?"}
```

## 💬 Ejemplos de preguntas y respuestas

**¿Cuáles son los requisitos para unirse al programa de afiliados?**
> Pueden postular creadores de contenido, sitios de cupones, medios digitales, comunidades de compras, educadores o reseñadores de productos y socios de contenido con audiencia en LATAM.

**¿Qué pasa si mi producto llega dañado?**
> Debes reportar el caso dentro de las 48 horas de la recepción. Puede aplicarse devolución, cambio o reemplazo sin necesidad de diagnóstico técnico, siempre que la evidencia sea suficiente.

**¿Qué opciones de envío tienen disponibles?**
> Envío estándar, express, programado, retiro en punto autorizado, reenvío por incidencia y recolección de devolución.

**¿Cuál es la garantía de los productos?**
> Cubre defectos de fabricación, materiales o ensamblaje no causados por el cliente. El plazo varía según tipo de producto y país.

## 📸 Interfaz de chat

![Chat BimBam Buy](docs/Captura_de_pantalla_2026-06-28_a_la_s__3_58_56_p_m_.png)
