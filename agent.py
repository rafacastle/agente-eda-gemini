from google import genai
from google.genai import types
import pandas as pd
import subprocess

class SistemaMultiAgenteEDA:
    def __init__(self, api_key: str, df: pd.DataFrame):
        self.client = genai.Client(api_key=api_key)
        self.df = df
        self.modelo = 'gemini-3.8-flash'

        # =================================================================
        # AGENTE 1: ESPECIALISTA EN DATOS (EDA)
        # =================================================================
        def ejecutar_agente_eda(instruccion_analitica: str) -> str:
            """Llama a este agente primero para explorar el DataFrame, ver columnas, nulos y estadísticas."""
            print(f"\n📊 [Agente EDA] Activado. Tarea: {instruccion_analitica}")
            
            def obtener_columnas() -> str:
                """Devuelve nombres de columnas y tipos de datos."""
                return "\n".join([f"{col}: {self.df[col].dtype}" for col in self.df.columns])
                
            def resumen_estadistico() -> str:
                """Devuelve estadísticas descriptivas numéricas."""
                return self.df.describe().to_string()
                
            def detectar_nulos() -> str:
                """Devuelve el conteo de valores nulos por columna."""
                nulos = self.df.isnull().sum()
                return nulos[nulos > 0].to_string() if not nulos[nulos > 0].empty else "Sin nulos."

            config_eda = types.GenerateContentConfig(
                system_instruction="Eres un Científico de Datos Senior. Analiza el dataset usando tus herramientas y devuelve un resumen técnico con cifras exactas.",
                temperature=0.0,
                tools=[obtener_columnas, resumen_estadistico, detectar_nulos]
            )
            chat_eda = self.client.chats.create(model=self.modelo, config=config_eda)
            respuesta = chat_eda.send_message(instruccion_analitica).text
            print("✅ [Agente EDA] Análisis finalizado y entregado al Manager.")
            return respuesta

        # =================================================================
        # AGENTE 2: INVESTIGADOR WEB Y REDACTOR DE REPORTES
        # =================================================================
        def ejecutar_agente_redactor(hallazgos_datos: str, nombre_archivo: str) -> str:
            """Llama a este agente segundo. Recibe los hallazgos del Agente EDA, investiga contexto en Google y guarda un reporte en un archivo Markdown (.md)."""
            print(f"\n📝 [Agente Redactor] Activado. Creando {nombre_archivo}...")

            def buscar_en_google(consulta: str) -> str:
                """Usa el buscador de Google para encontrar contexto real o histórico sobre el tema del dataset."""
                print(f"   🌐 [Agente Redactor -> Google Search] Buscando: '{consulta}'")
                res = self.client.models.generate_content(
                    model=self.modelo,
                    contents=consulta,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                return res.text

            def guardar_reporte_disco(contenido_markdown: str) -> str:
                """Guarda el reporte final en formato Markdown en el disco local del repositorio."""
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    f.write(contenido_markdown)
                print(f"   💾 [Agente Redactor] Archivo '{nombre_archivo}' guardado en el repositorio.")
                return f"Archivo {nombre_archivo} creado exitosamente."

            config_redactor = types.GenerateContentConfig(
                system_instruction="""Eres un Consultor Estratégico. 
                1. Toma los datos estadísticos que te pasen.
                2. Usa 'buscar_en_google' para contrastar un dato curioso con la realidad histórica.
                3. Redacta un reporte ejecutivo en Markdown bien estructurado y DEBES guardarlo usando 'guardar_reporte_disco'.""",
                temperature=0.2,
                tools=[buscar_en_google, guardar_reporte_disco]
            )
            chat_redactor = self.client.chats.create(model=self.modelo, config=config_redactor)
            prompt = f"Redacta y guarda el archivo '{nombre_archivo}' basado en estos hallazgos:\n{hallazgos_datos}"
            respuesta = chat_redactor.send_message(prompt).text
            print("✅ [Agente Redactor] Reporte documentado.")
            return respuesta

        # =================================================================
        # AGENTE 3: INGENIERO DEVOPS (GITHUB)
        # =================================================================
        def ejecutar_agente_git(nombre_reporte: str, mensaje_commit: str) -> str:
            """Llama a este agente al final para subir el archivo agent.py (sin modificar) y el nuevo reporte a GitHub."""
            print(f"\n🚀 [Agente Git] Activado. Preparando push a GitHub...")

            def subir_a_github(archivo_reporte: str, commit_msg: str) -> str:
                """Ejecuta git add, commit y push en la consola para agent.py y el reporte generado."""
                try:
                    # Agregamos explícitamente agent.py intacto y el nuevo reporte
                    subprocess.run(["git", "add", "agent.py", archivo_reporte], check=True)
                    
                    # Hacemos el commit
                    res_commit = subprocess.run(
                        ["git", "commit", "-m", commit_msg],
                        capture_output=True, text=True
                    )
                    
                    # Subimos a la rama main
                    res_push = subprocess.run(
                        ["git", "push", "origin", "main"],
                        capture_output=True, text=True, check=True
                    )
                    return f"Commit: {res_commit.stdout}\nPush exitoso a GitHub."
                except subprocess.CalledProcessError as e:
                    return f"Error en Git: {e.stderr or e.stdout}"

            config_git = types.GenerateContentConfig(
                system_instruction="Eres un ingeniero DevOps. Tu único trabajo es usar la herramienta 'subir_a_github' con un mensaje de commit profesional (ej. 'docs: agrega reporte EDA y actualiza agent.py').",
                temperature=0.0,
                tools=[subir_a_github]
            )
            chat_git = self.client.chats.create(model=self.modelo, config=config_git)
            prompt = f"Sube el reporte '{nombre_reporte}' y el código 'agent.py' a GitHub con el mensaje: {mensaje_commit}"
            respuesta = chat_git.send_message(prompt).text
            print("✅ [Agente Git] Operación en GitHub terminada.")
            return respuesta

        # =================================================================
        # EL CEREBRO ORQUESTADOR: AGENTE MANAGER
        # =================================================================
        instrucciones_manager = """
        Eres el Manager de un equipo de Ciencia de Datos compuesto por 3 agentes especialistas:
        1. 'ejecutar_agente_eda': Para analizar el DataFrame.
        2. 'ejecutar_agente_redactor': Para buscar contexto en Google y escribir el archivo Markdown.
        3. 'ejecutar_agente_git': Para subir 'agent.py' y el reporte generado al repositorio de GitHub.

        Coordina a tu equipo en orden secuencial. No inventes datos; pasa los hallazgos exactos del Agente 1 al Agente 2, y cuando el archivo esté creado, ordena al Agente 3 subirlo a GitHub. Al final, entrega un resumen ejecutivo al usuario.
        """

        config_manager = types.GenerateContentConfig(
            system_instruction=instrucciones_manager,
            temperature=0.1,
            tools=[ejecutar_agente_eda, ejecutar_agente_redactor, ejecutar_agente_git]
        )

        self.manager_chat = self.client.chats.create(model=self.modelo, config=config_manager)
        print("👔 [Manager Multi-Agente] Equipo inicializado y listo para recibir órdenes.")

    def ejecutar_proyecto(self, orden_usuario: str) -> str:
        return self.manager_chat.send_message(orden_usuario).text
