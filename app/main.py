"""Main entry point for the AI Document Intelligence application."""
from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.search import router as search_router

app = FastAPI(
    title="AI Document Intelligence API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI Document Intelligence API is running 🚀"}

# Health check endpoint to verify that the service is up and running
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "document-intelligence"
    }

app.include_router(upload_router)
app.include_router(search_router)
