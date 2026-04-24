from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nlp_engine import NLPEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Health Chatbot API")

# Setup CORS to allow the Vite frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the NLP Engine
engine = NLPEngine()

class ChatRequest(BaseModel):
    message: str
    knows_disease: bool = False

class ChatResponse(BaseModel):
    disease: str
    treatment: str
    confidence: float
    disclaimer: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = engine.predict(request.message, request.knows_disease)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Health Chatbot API is running"}
