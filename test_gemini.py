from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

respuesta = llm.invoke("Responde en español: ¿Qué es RAG en inteligencia artificial? En máximo 2 oraciones.")
print("✓ Gemini responde:")
print(respuesta.content)
