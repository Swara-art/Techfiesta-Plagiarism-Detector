import io
import mimetypes
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extract_text_from_plain
)
from app.text_analysis import perform_web_plagiarism_analysis, perform_semantic_analysis
from app.code_analysis import perform_code_analysis
from app.code_plagiarism import detect_github_plagiarism
from app.github_search import search_github_code, fetch_raw_file

router = APIRouter()

PLAINTEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".java", ".c", ".cpp", ".js", ".ts",
    ".html", ".css", ".json", ".yaml", ".yml", ".csv", ".ini",
    ".go", ".rs", ".swift", ".kt", ".php", ".rb"
}

# This file defines the API "router"
# It handles the /upload endpoint and calls the correct helpers.

def get_extension(filename: str) -> str:
    return "." + filename.split(".")[-1].lower() if "." in filename else ""

@router.post("/upload")
async def upload_file_and_analyze(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_stream = io.BytesIO(file_bytes)

    filename = file.filename or "uploaded"
    ext = get_extension(filename)
    content_type = file.content_type or mimetypes.guess_type(filename)[0]

    analysis_type = "semantic"  # default

    # --- 1. Handle known binary formats ---
    if ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_stream)

    elif ext == ".docx":
        extracted_text = extract_text_from_docx(file_stream)

    # --- 2. Python files → Code Analysis ---
    elif ext == ".py":
        extracted_text = extract_text_from_plain(file_stream)
        analysis_type = "code"

        from app.code_plagiarism import detect_github_plagiarism
        github_result = detect_github_plagiarism(extracted_text)

        internal_result = perform_code_analysis(extracted_text)

        return {
            "filename": filename,
            "type": "code",
            "github_analysis": github_result,
            "internal_analysis": internal_result
        }

    # --- 3. Known plaintext formats ---
    elif ext in PLAINTEXT_EXTENSIONS:
        extracted_text = extract_text_from_plain(file_stream)

    # --- 4. Unknown format → try to read as text ---
    else:
        try:
            extracted_text = extract_text_from_plain(file_stream)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported or unreadable file type: {ext}"
            )

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="File contains no readable text.")

    # --- 5. Decide Which Analyzer to Use ---
    if analysis_type == "code":
        results = perform_code_analysis(extracted_text)
    else:
        results = perform_semantic_analysis(extracted_text)

    return {
        "filename": filename,
        "type": analysis_type,
        "message": "Analysis complete.",
        **results
    }

@router.post("/analyze/web")
async def analyze_full_web(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = file_bytes.decode("utf-8", errors="ignore")

    internal = perform_internal_plagiarism_analysis(extracted_text)
    external = perform_external_plagiarism_analysis(extracted_text)

    return {
        "filename": file.filename,
        "type": "text",
        "internal_plagiarism": internal,
        "external_plagiarism": external
    }
