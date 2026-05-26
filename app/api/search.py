from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import generate_embeddings
from app.services.vector_store import search_similar_chunks
from app.services.llm_service import generate_answer
from app.services.memory_service import (
    add_message,
    get_conversation_context
)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/ask")
def ask_question(request: SearchRequest):

    # Generate query embedding
    query_embedding = generate_embeddings([request.query])

    # Retrieve relevant chunks
    results = search_similar_chunks(query_embedding)

    # Combine retrieved context
    context = "\n\n".join(results)

    #Get conversation history
    history = get_conversation_context()

    # Generate grounded answer
    answer = generate_answer(context, request.query, history)
    
    #Save assistant response
    add_message("assistant", answer)

    return {
        "question": request.query,
        "answer": answer,
        "retrieved_chunks": results
    }