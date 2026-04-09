import requests

class AIModule:
    def __init__(self, db=None):
        self.db = db

    def analyze(self, text):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",  # 🔥 puedes cambiar a "llama3" si quieres
                    "prompt": f"Eres un asistente médico. Responde claro y breve:\n{text}",
                    "stream": False
                }
            )

            result = response.json()
            print("DEBUG OLLAMA:", result)  # 👈 IMPORTANTE PARA DEBUG

            # ✅ Manejo seguro de respuesta
            answer = result.get("response", str(result))

            return {
                "diagnosis": answer
            }

        except Exception as e:
            print("Error con Ollama:", e)
            return {
                "diagnosis": "No pude procesar la solicitud."
            }