from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

respuesta = llm.invoke("Responde en español: ¿Qué es RAG en inteligencia artificial? En máximo 2 oraciones.")
print("✓ Groq responde:")
print(respuesta.content)
