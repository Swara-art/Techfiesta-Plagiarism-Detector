from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv

from app.api.routes.health import router as health_router
from app.api.routes.assignments import router as assignments_router
from app.api.routes.analysis import router as analysis_router
from app.db.chroma_collections import init_chroma_collections

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="ED007 - Plagiarism & Authenticity Checker")

# ✅ CORS Middleware (REQUIRED for frontend ↔ backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Startup event
@app.on_event("startup")
def startup_event():
    print("CHROMA_API_KEY loaded:", bool(os.getenv("CHROMA_API_KEY")))
    init_chroma_collections()

# ✅ API Routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(assignments_router, prefix="/assignments", tags=["assignments"])
app.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
