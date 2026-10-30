import seaborn as sns
import importlib
import agent

def ejecutar_flujo_eda(api_key: str):
    print("🎬 [Orquestador EDA] Iniciando flujo de trabajo...")
    
    # Forzamos lectura fresca del módulo agent.py
    importlib.reload(agent)
    from agent import SistemaMultiAgenteEDA
    
    # 1. Carga de datos
    df = sns.load_dataset('titanic')
    
    # 2. Instanciación del Manager y su equipo
    equipo = SistemaMultiAgenteEDA(api_key=api_key, df=df)
    
    # 3. Orden de trabajo
    orden = """
    1. Pídele al agente de EDA que analice la edad promedio, la tarifa promedio (fare) y los nulos del dataset.
    2. Pídele al redactor que contraste esos datos buscando en Google cuánto costaba realmente un boleto del Titanic en 1912, y que guarde todo en un archivo llamado 'REPORTE_TITANIC.md'.
    3. Pídele al agente de Git que suba tanto 'agent.py' como 'REPORTE_TITANIC.md' a nuestro repositorio de GitHub.
    """
    
    resultado = equipo.ejecutar_proyecto(orden)
    print("\n=== RESPUESTA FINAL DEL ORQUESTADOR EDA ===")
    print(resultado)
