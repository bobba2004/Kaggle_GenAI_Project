# vector_store.py
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import chromadb

def setup_vector_db(chunks, persist_directory="./chroma_db"):
    """Create and populate a vector database from document chunks."""
    # Set up embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create vector store
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Persist to disk
    db.persist()
    
    return db

def load_vector_db(persist_directory="./chroma_db"):
    """Load an existing vector database."""
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return db
