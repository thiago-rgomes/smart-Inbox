from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.services.file_reader import extract_text
from backend.services.ai_service import classify_email_ai, generate_response_ai


app = FastAPI()

# =====================================================
# FRONTEND ESTÁTICO
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# API
# =====================================================

@app.post("/process-email")
async def process_email(
    text: str = Form(None),
    file: UploadFile = None
):
    email_text = ""

    if text:
        email_text += text

    if file:
        email_text += "\n" + extract_text(file)

    if not email_text.strip():
        return {"error": "Nenhum conteúdo fornecido"}

    classification = classify_email_ai(email_text)
    response = generate_response_ai(email_text, classification)

    return {
        "classification": classification,
        "suggested_response": response
    }