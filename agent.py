from google import genai
import pandas as pd

class EDA_Agent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        # Usamos gemini-2.5-flash (o gemini-2.0-flash)
        self.model_id = 'gemini-2.5-flash'
        print("🤖 Cerebro Gemini inicializado con la NUEVA API (google-genai).")

    def test_connection(self):
        """Un método simple para probar que el LLM responde."""
        respuesta = self.client.models.generate_content(
            model=self.model_id,
            contents="Eres un agente científico de datos. Saluda en 1 oración."
        )
        return respuesta.text
