from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from modules.ai_module import AIModule
from modules.db_module import MedicalDB
from modules.knowledge_loader import load_knowledge

app = FastAPI()

# ✅ CORS (bien configurado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Inicializar TODO UNA VEZ
db = MedicalDB()
db.seed_data()

knowledge = load_knowledge("knowledge")
ai = AIModule(db, knowledge)


# ==============================
# 🔹 MODELO ORIGINAL
# ==============================

class Query(BaseModel):
    prompt: str


# ==============================
# 🔹 ENDPOINT ORIGINAL (tuyo)
# ==============================

@app.post("/chat")
def chat(query: Query):
    try:
        result = ai.analyze(query.prompt)

        if isinstance(result, dict):
            return result
        else:
            return {"response": str(result)}

    except Exception as e:
        return {"error": str(e)}


# ==============================
# 🔥 OPENAI COMPATIBLE (FIXED)
# ==============================

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()

        # 🔥 Seguridad por si viene mal el request
        messages = body.get("messages", [])
        if not messages:
            return {"error": "No messages provided"}

        user_message = messages[-1].get("content", "")

        result = ai.analyze(user_message)

        # 🔥 MANEJO ROBUSTO (esto evita el 500)
        if isinstance(result, dict):
            response_text = (
                result.get("diagnosis")
                or result.get("response")
                or str(result)
            )
        else:
            response_text = str(result)

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

    except Exception as e:
        return {
            "error": str(e)
        }


# ==============================
# 🔹 MODELOS (necesario para WebUI)
# ==============================

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