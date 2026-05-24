from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid
from app.services.pdf_service import extract_text_from_pdf

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


    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "path": str(file_path),
        "characters_extracted": len(extracted_text),
        "preview": extracted_text[:400]  # Return first 400 
    }