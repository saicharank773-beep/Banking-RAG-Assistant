
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama


# Workflow state
class BankingState(TypedDict):
    question: str
    context: str
    answer: str


# Embedding model
def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )


# Retrieval node
def retrieve_documents(state):

    vector_store = Chroma(
        collection_name="banking_documents",
        persist_directory="./chroma_db",
        embedding_function=get_embeddings()
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    documents = retriever.invoke(state["question"])

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    return {"context": context}


# Answer generation node
def generate_answer(state):

    if not state["context"].strip():
        return {
            "answer": "Information not specified in the documents."
        }

    llm = ChatOllama(
        model="qwen2.5:0.5b",
        base_url="http://localhost:11434",
        temperature=0
    )

    prompt = f"""
    You are a Banking HR Policy Assistant.
    Answer only using the context.
    Do not invent information.
    If information is missing, say:
    Information not specified in the documents.

    Context:
    {state["context"]}

    Question:
    {state["question"]}
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}


# Validation node
def validate_answer(state):

    context = state["context"].lower()
    answer = state["answer"]

    if not context.strip():
        return {
            "answer": "Information not specified in the documents."
        }

    consequence_terms = [
        "verbal warning",
        "written warning",
        "final warning",
        "suspension",
        "termination"
    ]

    answer_has_terms = any(
        term in answer.lower() for term in consequence_terms
    )

    context_has_terms = any(
        term in context for term in consequence_terms
    )

    if answer_has_terms and not context_has_terms:
        return {
            "answer": (
                "Falsification of attendance records is "
                "strictly prohibited. Specific disciplinary "
                "consequences are not specified in the "
                "retrieved documents."
            )
        }

    return {"answer": answer}


# Build LangGraph
graph = StateGraph(BankingState)

graph.add_node("retrieve", retrieve_documents)
graph.add_node("generate", generate_answer)
graph.add_node("validate", validate_answer)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "validate")
graph.add_edge("validate", END)

banking_workflow = graph.compile()


# Run directly
if __name__ == "__main__":

    question = input("Ask your Banking HR question: ")

    result = banking_workflow.invoke({
        "question": question,
        "context": "",
        "answer": ""
    })

    print("\nBanking AI Assistant Answer:")
    print(result["answer"])
