from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import store_embeddings


router = APIRouter()

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Validate PDF
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    file_path = UPLOAD_DIR / unique_filename

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Close the file after saving
    

    # Extract PDF text.
    extracted_text = extract_text_from_pdf(str(file_path))

    # Chunk the extracted text.
    chunks = chunk_text(extracted_text)


    # Generate embeddings for the chunks.
    embeddings = generate_embeddings(chunks)

    # Store chunks and embeddings in vector store.
    store_embeddings(chunks, embeddings)

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "path": str(file_path), # T..D: (Would be a mistake in production)
        "chunks_created": len(chunks),
        "embeddings_generated": len(embeddings), # T..D
        "characters_extracted": len(extracted_text), # T..D
        "preview": extracted_text[:400]  # Return first 400 
    }