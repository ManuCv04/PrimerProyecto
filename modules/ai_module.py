import requests

class AIModule:
    def __init__(self, db):
        self.db = db
        self.url = "http://localhost:11434/api/generate"

    def analyze(self, text):
        prompt = f"""
Eres un asistente médico.

Analiza el siguiente síntoma del paciente:

"{text}"

Responde en este formato EXACTO:

Diagnóstico posible:
(una explicación clara)

Nivel:
(Leve, Moderado o Grave)

Recomendaciones:
- tratamiento 1
- tratamiento 2
- tratamiento 3

Si es grave, indica acudir a emergencias.
"""

        response = requests.post(self.url, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })

        data = response.json()

        return {
            "diagnosis": data["response"],
            "recommendation": []
        }