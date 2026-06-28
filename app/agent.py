from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def cargar_agente():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vector_store = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = PromptTemplate(
        template="""Eres un asistente virtual de BimBam Buy, una tienda de e-commerce.
Responde en español usando ÚNICAMENTE la información del contexto proporcionado.
Si la respuesta no está en el contexto, di claramente: "No tengo información sobre ese tema en los documentos de BimBam Buy."

Contexto:
{context}

Pregunta: {question}

Respuesta:""",
        input_variables=["context", "question"]
    )

    agente = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 6}),
        chain_type_kwargs={"prompt": prompt}
    )

    return agente

if __name__ == "__main__":
    print("🤖 Cargando agente BimBam Buy...")
    agente = cargar_agente()
    print("✓ Agente listo\n")

    preguntas = [
        "¿Cuál es la política de reembolsos?",
        "¿Cuánto tiempo tarda un envío estándar?",
        "¿Qué métodos de pago aceptan?"
    ]

    for pregunta in preguntas:
        print(f"❓ {pregunta}")
        respuesta = agente.invoke({"query": pregunta})
        print(f"💬 {respuesta['result']}\n")
        print("-" * 50 + "\n")
