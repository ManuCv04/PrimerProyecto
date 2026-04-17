from fastapi import FastAPI, Request
from pydantic import BaseModel

from modules.ai_module import AIModule
from modules.db_module import MedicalDB
from modules.knowledge_loader import load_knowledge

app = FastAPI()

# 🔥 Inicializar TODO UNA VEZ
db = MedicalDB()
db.seed_data()

knowledge = load_knowledge("knowledge")
ai = AIModule(db, knowledge)


# 🔹 Modelo de entrada original
class Query(BaseModel):
    prompt: str


# 🔹 Endpoint original (tuyo)
@app.post("/chat")
def chat(query: Query):
    result = ai.analyze(query.prompt)
    return result


# ==============================
# 🔥 NUEVO: COMPATIBLE OPENAI
# ==============================

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()

    user_message = body["messages"][-1]["content"]

    result = ai.analyze(user_message)
    response_text = result["diagnosis"]

    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }
        ]
    }


@app.get("/v1/models")
async def get_models():
    return {
        "data": [
            {
                "id": "gpt-3.5-turbo",
                "object": "model"
            }
        ]
    }