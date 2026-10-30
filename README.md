# 🤖 Agente EDA & Metaprogramación Controlada con Gemini

Este repositorio implementa una arquitectura de **Agentes de Inteligencia Artificial desde cero** (sin frameworks pesados de terceros), utilizando Python puro y la nueva SDK oficial de Google (`google-genai`) en su capa gratuita desde **Google Colab**.

El proyecto demuestra dos patrones avanzados de ingeniería de agentes en producción:
1. **Orquestación Multi-Agente Jerárquica (Hierarchical Function Calling)** para Ciencia de Datos (EDA), investigación web en tiempo real y automatización DevOps en GitHub.
2. **Agentes Auto-Modificables Controlados (Self-Modifying Agents)** capaces de reescribir su propio código fuente en disco y recargarse en memoria RAM en caliente (*Hot-Reloading*).

---

## 🏗️ Arquitectura del Proyecto (Patrón *Thin Notebook*)

El repositorio sigue la buena práctica de mantener los Notebooks de Colab únicamente como consolas de ejecución ligeras (*Thin Notebooks*), encapsulando toda la lógica en módulos `.py` versionables:

```text
agente-eda-gemini/
│
├── agent.py                 # Motor del Sistema Multi-Agente (Manager + 3 Especialistas)
├── orquestador_eda.py       # Flujo de carga de datos (Titanic) y ejecución del equipo EDA
├── agente_mutante.py        # Agente capaz de reescribir su propio código mediante catálogo cerrado
├── orquestador_mutante.py   # Controlador de mutación y trasplante en memoria RAM (importlib)
├── REPORTE_TITANIC.md       # Reporte ejecutivo generado y subido autónomamente por los agentes
└── README.md                # Documentación del repositorio
```

---

## 🧠 1. Sistema Multi-Agente de Ciencia de Datos (`agent.py`)

En lugar de saturar a un solo modelo con decenas de funciones, el sistema utiliza un **Agente Manager** cuyas únicas herramientas son invocar a tres agentes especialistas en orden secuencial:

* 📊 **Agente 1 (`AgenteEDA`):** Conecta directamente con el `DataFrame` de Pandas en memoria para auditar tipos de datos, valores nulos y estadística descriptiva.
* 🌐 **Agente 2 (`AgenteRedactor`):** Recibe las métricas crudas del Agente 1, utiliza la herramienta nativa de **Google Search** para contrastar los hallazgos con datos históricos reales y redacta un informe en disco (`REPORTE_TITANIC.md`).
* 🚀 **Agente 3 (`AgenteGit`):** Opera sobre la terminal Linux de Colab (`subprocess`) para ejecutar `git add`, `git commit` y `git push`, subiendo al repositorio tanto el reporte recién creado como su propio código fuente intacto.

---

## 🧬 2. Agente Auto-Modificable de Opción Múltiple (`agente_mutante.py`)

Demostración segura de **Metaprogramación Recursiva**:
* **Zona Quirúrgica Delimitada:** El agente solo tiene permiso para reescribir la función `procesar_datos()` ubicada entre marcadores estrictos dentro de su propio archivo `.py`.
* **Catálogo Cerrado (Guardrail contra errores de sintaxis):** El LLM no improvisa código libre; evalúa la necesidad del usuario y elige entre plantillas pre-aprobadas (`MODO_ESTADISTICO`, `MODO_FINANCIERO`, `MODO_AUDITOR`).
* **Recarga en Caliente (*Hot-Reload*):** `orquestador_mutante.py` utiliza `importlib.reload()` para actualizar el comportamiento del agente en la memoria RAM sin necesidad de reiniciar el entorno de Google Colab.

---

## ⚙️ Requisitos y Configuración en Google Colab

1. Configura tus credenciales en el panel **Secrets** (🔑) de Google Colab:
   * `GEMINI_API_KEY`: Tu llave de Google AI Studio.
   * `GITHUB_TOKEN`: Tu Personal Access Token (Classic) con permisos `repo`.
2. Instala las dependencias en el entorno:
```bash
pip install -q -U google-genai seaborn pandas
```
3. Ejecuta los flujos desde el Notebook llamando a los orquestadores:
```python
from google.colab import userdata
import orquestador_eda
import orquestador_mutante

GEMINI_KEY = userdata.get('GEMINI_API_KEY')

# Ejecutar experimento de auto-modificación
orquestador_mutante.ejecutar_experimento_mutacion(
    api_key=GEMINI_KEY,
    peticion_usuario="Calcula el total sumando el IVA.",
    datos_prueba=[100, 250, -50, 400]
)

# Ejecutar el equipo Multi-Agente EDA + GitHub Push
orquestador_eda.ejecutar_flujo_eda(api_key=GEMINI_KEY)
```
