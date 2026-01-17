from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from services.file_reader import extract_text
from services.ai_service import classify_email_ai, generate_response_ai


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

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