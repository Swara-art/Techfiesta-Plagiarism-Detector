# Post/upload api endpoint
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import PyPDF2
import docx
import io
import mimetypes
from app.utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from app.api import router
from app.code_analysis import perform_code_analysis

import os
print(os.getenv("TAVILY_API_KEY"))

#Create fastapi app
app = FastAPI(title="Plagiarism Checker API", 
              description="API to check plagiarism in uploaded documents", 
              version="0.1.0"
            )

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    