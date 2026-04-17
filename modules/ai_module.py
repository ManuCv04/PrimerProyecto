class AIModule:
    def __init__(self, db, knowledge):
        self.db = db
        self.knowledge = knowledge

    def analyze(self, text):
        # 🔥 PROMPT MÉDICO CONTROLADO
        prompt = f"""
Eres un asistente médico profesional.

Responde SOLO usando la siguiente base de conocimiento.
Si la respuesta no está en la información, responde:
"No tengo suficiente información médica para responder con precisión."

BASE DE CONOCIMIENTO:
{self.knowledge}

PREGUNTA:
{text}
"""

        # 🔥 AQUÍ LLAMAS A OLLAMA (o tu modelo)
        import requests

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )

            result = response.json()
            answer = result.get("response", "No se pudo generar respuesta.")

        except Exception as e:
            answer = f"Error conectando con IA: {e}"

        return {
            "diagnosis": answer
        }