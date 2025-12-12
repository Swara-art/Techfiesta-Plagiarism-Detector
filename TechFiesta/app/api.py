import io
import mimetypes
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_plain
)

from app.text_analysis import perform_text_plagiarism_analysis
from app.code_analysis import perform_code_analysis
from app.code_plagiarism import detect_github_plagiarism

router = APIRouter()

PLAINTEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".java", ".c", ".cpp", ".js", ".ts",
    ".html", ".css", ".json", ".yaml", ".yml", ".csv", ".ini",
    ".go", ".rs", ".swift", ".kt", ".php", ".rb"
}


def get_extension(filename: str) -> str:
    return "." + filename.split(".")[-1].lower() if "." in filename else ""


@router.post("/upload")
async def upload_file_and_analyze(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_stream = io.BytesIO(file_bytes)

    filename = file.filename or "uploaded"
    ext = get_extension(filename)
    content_type = file.content_type or mimetypes.guess_type(filename)[0]

    # -----------------------------
    # 1. Extract text
    # -----------------------------

    if ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_stream)

    elif ext == ".docx":
        extracted_text = extract_text_from_docx(file_stream)

    elif ext in PLAINTEXT_EXTENSIONS:
        extracted_text = extract_text_from_plain(file_stream)

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported or unreadable file type: {ext}"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="File contains no readable text."
        )

    # -----------------------------
    # 2. Code plagiarism pipeline
    # -----------------------------

    if ext == ".py":
        github_result = detect_github_plagiarism(extracted_text)
        internal_result = perform_code_analysis(extracted_text)

        return {
            "filename": filename,
            "type": "code",
            "github_analysis": github_result,
            "internal_analysis": internal_result
        }

    # -----------------------------
    # 3. Text plagiarism pipeline
    # -----------------------------

    results = perform_text_plagiarism_analysis(extracted_text)

    return {
        "filename": filename,
        "type": "text",
        "message": "Analysis complete.",
        **results
    }


@router.post("/analyze/web")
async def analyze_full_web(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = file_bytes.decode("utf-8", errors="ignore")

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="File contains no readable text."
        )

    results = perform_text_plagiarism_analysis(extracted_text)

    return {
        "filename": file.filename,
        "type": "text",
        **results
    }
