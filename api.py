from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask_question

app = FastAPI(title="Banking AI Assistant API")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Banking AI Assistant API is running"}


@app.post("/ask")
def ask(request: QuestionRequest):
    answer = ask_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }