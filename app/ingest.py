from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def crear_vector_store():
    print("📄 Cargando PDFs...")
    loader = PyPDFDirectoryLoader("data/pdfs/")
    documentos = loader.load()
    print(f"✓ {len(documentos)} páginas cargadas")

    print("✂️  Dividiendo en fragmentos...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    fragmentos = splitter.split_documents(documentos)
    print(f"✓ {len(fragmentos)} fragmentos creados")

    print("🔢 Creando embeddings y vector store...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    vector_store = FAISS.from_documents(fragmentos, embeddings)
    vector_store.save_local("data/faiss_index")
    print("✓ Vector store guardado en data/faiss_index")
    return vector_store

if __name__ == "__main__":
    crear_vector_store()
