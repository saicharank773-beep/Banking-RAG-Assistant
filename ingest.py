
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Load PDF documents
def load_documents():

    documents = []

    for pdf in Path("documents").glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        documents.extend(loader.load())
        print("Loaded:", pdf.name)

    print("Total pages:", len(documents))

    return documents


# 2. Split documents into chunks
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks:", len(chunks))

    return chunks


# 3. Generate embeddings
def get_embeddings():

    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )


# 4. Store documents in ChromaDB
def create_vector_store(chunks):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory="./chroma_db",
        collection_name="banking_documents"
    )

    print("Documents stored successfully!")

    return vector_store


# 5. Run ingestion pipeline
if __name__ == "__main__":

    documents = load_documents()

    if documents:
        chunks = split_documents(documents)
        create_vector_store(chunks)
        print("PDF ingestion completed!")
    else:
        print("No PDF documents found.")
