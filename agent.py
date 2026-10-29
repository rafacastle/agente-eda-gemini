from google import genai
from google.genai import types
import pandas as pd

class EDA_Agent:
    def __init__(self, api_key: str, df: pd.DataFrame):
        self.client = genai.Client(api_key=api_key)
        self.df = df

        # ==========================================
        # ZONA DE HERRAMIENTAS (Function Calling)
        # ==========================================
        def obtener_columnas() -> str:
            """Usa esta herramienta al inicio para conocer las columnas y tipos de datos del dataset."""
            buffer = [f"{col}: {self.df[col].dtype}" for col in self.df.columns]
            return "\n".join(buffer)

        def resumen_estadistico() -> str:
            """Usa esta herramienta para calcular la media, desviación estándar, percentiles, mínimos y máximos numéricos."""
            # .to_string() es crucial para devolver texto plano al LLM, no un objeto Pandas
            return self.df.describe().to_string()

        def detectar_nulos() -> str:
            """Usa esta herramienta para saber si hay datos faltantes (NaN/Null) en las columnas."""
            nulos = self.df.isnull().sum()
            # Filtramos para mostrarle al agente solo las columnas que SÍ tienen nulos
            columnas_con_nulos = nulos[nulos > 0]
            if columnas_con_nulos.empty:
                return "No hay valores nulos en el dataset."
            return columnas_con_nulos.to_string()

        # ==========================================
        # CONFIGURACIÓN DEL CEREBRO
        # ==========================================
        instrucciones_sistema = """
        Eres un agente experto en Ciencia de Datos. Tu objetivo es realizar Análisis Exploratorio de Datos (EDA).
        Tus respuestas deben ser analíticas, directas y enfocadas en hallazgos estadísticos que generen valor de negocio.
        Siempre revisa la estructura, los nulos y la estadística descriptiva antes de sacar conclusiones.
        """

        config = types.GenerateContentConfig(
            system_instruction=instrucciones_sistema,
            temperature=0.0, # 0.0 garantiza respuestas estrictamente analíticas, sin alucinaciones
            # Pasamos la lista de todas las herramientas disponibles
            tools=[obtener_columnas, resumen_estadistico, detectar_nulos],
        )

        self.chat = self.client.chats.create(model='gemini-3.8-flash', config=config)

    def interactuar(self, mensaje: str):
        return self.chat.send_message(mensaje).text
