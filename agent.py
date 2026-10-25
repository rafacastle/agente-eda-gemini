from google import genai
from google.genai import types
import pandas as pd

class EDA_Agent:
    def __init__(self, api_key: str, df: pd.DataFrame):
        self.client = genai.Client(api_key=api_key)
        self.df = df 
        
        def obtener_informacion_columnas() -> str:
            """Usa esta herramienta SIEMPRE para descubrir los nombres de las columnas y sus tipos de datos antes de hacer un análisis."""
            buffer = []
            for col in self.df.columns:
                buffer.append(f"{col}: {self.df[col].dtype}")
            return "\n".join(buffer)

        instrucciones_sistema = """
        Eres un agente experto en Ciencia de Datos de nivel Senior. 
        Tu objetivo es realizar Análisis Exploratorio de Datos (EDA).
        Tus respuestas deben ser analíticas, directas y enfocadas en hallazgos estadísticos.
        """
        
        config = types.GenerateContentConfig(
            system_instruction=instrucciones_sistema,
            temperature=0.1,
            tools=[obtener_informacion_columnas], 
        )
        
        # Actualizamos a la versión 3.8-flash indicada por la API para uso gratuito
        self.chat = self.client.chats.create(
            model='gemini-3.8-flash', 
            config=config
        )
        print("🤖 Cerebro Gemini inicializado con Gemini 3.8 Flash (capa gratuita).")

    def interactuar(self, mensaje: str):
        respuesta = self.chat.send_message(mensaje)
        return respuesta.text
