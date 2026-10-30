import importlib
import agente_mutante

def ejecutar_experimento_mutacion(api_key: str, peticion_usuario: str, datos_prueba: list):
    print("🧪 [Orquestador Mutante] Iniciando experimento de auto-modificación...")
    
    # 1. Cargamos la versión actual del agente
    importlib.reload(agente_mutante)
    agente_v1 = agente_mutante.AgenteMutante(api_key=api_key)
    
    print("\n--- 1. COMPORTAMIENTO ANTES DE MUTAR ---")
    print(agente_v1.probar_habilidad(datos_prueba))
    
    # 2. El agente evalúa la petición, escoge del menú múltiple y reescribe agente_mutante.py
    print(f"\n--- 2. ORDENANDO EVOLUCIÓN: '{peticion_usuario}' ---")
    respuesta_llm = agente_v1.solicitar_evolucion(peticion_usuario)
    print(f"🤖 Respuesta del Agente: {respuesta_llm}")
    
    # 3. TRASPLANTE EN CALIENTE: Recargamos el archivo .py recién modificado en disco a la RAM
    importlib.reload(agente_mutante)
    agente_v2 = agente_mutante.AgenteMutante(api_key=api_key)
    
    print("\n--- 3. COMPORTAMIENTO DESPUÉS DE MUTAR (NUEVO CÓDIGO EN RAM) ---")
    print(agente_v2.probar_habilidad(datos_prueba))
