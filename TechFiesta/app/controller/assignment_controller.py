from fastapi import APIRouter, UploadFile, File
from utils.text_extraction import extract_text
from utils.sentence_segmentation import segment_sentences

router = APIRouter()


@router.post("/assignments/upload")
async def upload_assignment(file: UploadFile = File(...)):
    # Extract text
    text = extract_text(file)
    print("Extracted text length:", len(text))

    # Segment sentences
    sentences = segment_sentences(text)
    print("Segmented sentences:", len(sentences))

    return {
        "extracted_text_preview": text[:500],
        "total_sentences": len(sentences),
        "sentences": sentences[:10]  
    }
