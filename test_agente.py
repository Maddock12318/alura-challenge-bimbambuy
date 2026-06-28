from dotenv import load_dotenv
from app.agent import cargar_agente

load_dotenv()

agente = cargar_agente()
print("✓ Agente listo\n")

preguntas = [
    "¿Cuáles son los tiempos de entrega?",
    "¿Qué opciones de envío tienen disponibles?",
    "¿Aceptan tarjetas de crédito?",
    "¿Cómo funciona el programa de afiliados?",
    "¿Cuál es la garantía de los productos?"
]

for pregunta in preguntas:
    print(f"❓ {pregunta}")
    respuesta = agente.invoke({"query": pregunta})
    print(f"💬 {respuesta['result']}\n")
    print("-" * 50 + "\n")
