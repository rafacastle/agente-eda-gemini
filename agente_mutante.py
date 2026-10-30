from google import genai
from google.genai import types

# ==========================================================
# ZONA QUIRÚRGICA: ESTA FUNCIÓN SERÁ REESCRITA POR EL AGENTE
# ==========================================================
# ===ZONA_MUTABLE_INI===
def procesar_datos(numeros: list) -> str:
    total = sum(numeros)
    con_iva = total * 1.16
    return f"[MODO FINANCIERO ACTIVO] Subtotal: ${total:,.2f} | Total con IVA (16%): ${con_iva:,.2f}"
# ===ZONA_MUTABLE_FIN===


# Catálogo cerrado de mutaciones permitidas (Opción Múltiple)
CATALOGO_MUTACIONES = {
    "MODO_ESTADISTICO": '''def procesar_datos(numeros: list) -> str:
    promedio = sum(numeros) / len(numeros)
    return f"[MODO ESTADÍSTICO ACTIVO] Promedio: {promedio:.2f} | Máximo: {max(numeros)} | Mínimo: {min(numeros)}"''',

    "MODO_FINANCIERO": '''def procesar_datos(numeros: list) -> str:
    total = sum(numeros)
    con_iva = total * 1.16
    return f"[MODO FINANCIERO ACTIVO] Subtotal: ${total:,.2f} | Total con IVA (16%): ${con_iva:,.2f}"''',

    "MODO_AUDITOR": '''def procesar_datos(numeros: list) -> str:
    negativos = [n for n in numeros if n < 0]
    return f"[MODO AUDITOR ACTIVO] Total registros: {len(numeros)} | Alertas de valores negativos: {len(negativos)} ({negativos})"'''
}


class AgenteMutante:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.modelo = 'gemini-3.8-flash'

        def mutar_mi_codigo(opcion_elegida: str) -> str:
            """
            Modifica el código fuente de agente_mutante.py.
            PARAMETRO OBLIGATORIO 'opcion_elegida': Debe ser EXACTAMENTE una de estas 3 opciones:
            - 'MODO_ESTADISTICO': Si el usuario necesita promedios, máximos y mínimos.
            - 'MODO_FINANCIERO': Si el usuario habla de dinero, precios o impuestos (IVA).
            - 'MODO_AUDITOR': Si el usuario quiere detectar anomalías o números negativos.
            """
            if opcion_elegida not in CATALOGO_MUTACIONES:
                return f"Error: Opción '{opcion_elegida}' no válida. Elige entre {list(CATALOGO_MUTACIONES.keys())}"

            # Construimos los marcadores dinámicamente para no reemplazar esta misma línea de código
            marcador_ini = "# " + "===ZONA_MUTABLE_INI==="
            marcador_fin = "# " + "===ZONA_MUTABLE_FIN==="

            with open("agente_mutante.py", "r", encoding="utf-8") as f:
                codigo_actual = f.read()

            idx_ini = codigo_actual.find(marcador_ini)
            idx_fin = codigo_actual.find(marcador_fin)

            if idx_ini == -1 or idx_fin == -1:
                return "Error crítico: No se encontraron los marcadores de mutación."

            # Ensamblamos el nuevo archivo .py inyectando la opción elegida
            nuevo_bloque = f"{marcador_ini}\n{CATALOGO_MUTACIONES[opcion_elegida]}\n"
            codigo_mutado = codigo_actual[:idx_ini] + nuevo_bloque + codigo_actual[idx_fin:]

            with open("agente_mutante.py", "w", encoding="utf-8") as f:
                f.write(codigo_mutado)

            print(f"🧬 [Auto-Modificación] 'agente_mutante.py' reescrito con éxito -> {opcion_elegida}")
            return f"Éxito: Código fuente actualizado a {opcion_elegida}."

        config = types.GenerateContentConfig(
            system_instruction="""Eres un agente adaptable. Tu única tarea cuando el usuario te pida cambiar tu comportamiento 
            es analizar su necesidad, escoger la opción correcta del catálogo usando la herramienta 'mutar_mi_codigo' y confirmar qué opción elegiste.""",
            temperature=0.0,
            tools=[mutar_mi_codigo]
        )

        self.chat = self.client.chats.create(model=self.modelo, config=config)

    def probar_habilidad(self, lista_numeros: list) -> str:
        """Ejecuta la función que el agente tiene programada actualmente en su código."""
        return procesar_datos(lista_numeros)

    def solicitar_evolucion(self, necesidad_usuario: str) -> str:
        """Le pide al cerebro LLM que elija una mutación según la necesidad."""
        return self.chat.send_message(necesidad_usuario).text
