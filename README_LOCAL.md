# 🔬 Deep Research con API Local y DuckDuckGo

Este README explica cómo configurar y usar el sistema Deep Research con tu API local (LM Studio) y DuckDuckGo como motor de búsqueda, sin necesidad de APIs externas costosas.

## 🚀 Características

- ✅ **API Local**: Usa tu modelo local (LM Studio) en lugar de APIs externas
- ✅ **Búsqueda Gratuita**: DuckDuckGo como motor de búsqueda sin costos
- ✅ **Sin Autenticación**: Configuración simplificada para desarrollo local
- ✅ **Investigación Profunda**: Sistema completo de investigación automatizada
- ✅ **Interfaz Web**: LangGraph Studio para interacción fácil

## 📋 Requisitos Previos

### 1. LM Studio
- Instala [LM Studio](https://lmstudio.ai/)
- Carga un modelo compatible (ej: `openai/gpt-oss-20b`)
- Inicia el servidor en `localhost:1234`

### 2. Python y Dependencias
```bash
# Instalar dependencias
uv sync
# o
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Archivo de Configuración

El archivo `config_local.env` contiene toda la configuración necesaria:

```env
# Configuración del modelo local (localhost:1234)
RESEARCH_MODEL=openai:http://localhost:1234/v1
SUMMARIZATION_MODEL=openai:http://localhost:1234/v1
COMPRESSION_MODEL=openai:http://localhost:1234/v1
FINAL_REPORT_MODEL=openai:http://localhost:1234/v1

# API Key para el modelo local - usar cualquier valor ya que tu API acepta cualquier clave
OPENAI_API_KEY=test-key

# Configuración de búsqueda - usar DuckDuckGo en lugar de Tavily
SEARCH_API=duckduckgo

# Configuración de tokens
RESEARCH_MODEL_MAX_TOKENS=10000
SUMMARIZATION_MODEL_MAX_TOKENS=8192
COMPRESSION_MODEL_MAX_TOKENS=8192
FINAL_REPORT_MODEL_MAX_TOKENS=10000

# Configuración de investigación
MAX_CONCURRENT_RESEARCH_UNITS=3
MAX_RESEARCHER_ITERATIONS=4
MAX_REACT_TOOL_CALLS=8
MAX_STRUCTURED_OUTPUT_RETRIES=3

# Configuración de contenido
MAX_CONTENT_LENGTH=50000

# Configuración de clarificación
ALLOW_CLARIFICATION=true
```

### 2. Verificar API Local

Antes de usar el sistema, verifica que tu API local esté funcionando:

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.7,
    "max_tokens": 10,
    "stream": false
}'
```

## 🚀 Uso

### Opción 1: Script de Inicio Automático

```bash
# Hacer ejecutable
chmod +x start_local_dev.sh

# Ejecutar
./start_local_dev.sh
```

### Opción 2: Comando Manual

```bash
# Cargar configuración
export $(grep -v '^#' config_local.env | xargs)

# Iniciar servidor
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking --auth ./src/security/auth_local.py:auth
```

### Opción 3: Sin Autenticación (Recomendado para desarrollo)

```bash
# Usar autenticación local simplificada
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking --auth ./src/security/auth_local.py:auth
```

## 🌐 Acceso a la Interfaz

Una vez iniciado el servidor:

- **API**: http://127.0.0.1:2024
- **Studio UI**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- **API Docs**: http://127.0.0.1:2024/docs

### Configuración en la Interfaz

1. Abre el Studio UI
2. Ve a "Manage Assistants"
3. Configura:
   - **Search API**: `DuckDuckGo`
   - **Research Model**: `openai:http://localhost:1234/v1`
   - **Summarization Model**: `openai:http://localhost:1234/v1`
   - **Compression Model**: `openai:http://localhost:1234/v1`
   - **Final Report Model**: `openai:http://localhost:1234/v1`

## 🧪 Pruebas

### Script de Prueba Automático

```bash
python3 test_local_config.py
```

Este script verifica:
- ✅ Conexión a API local
- ✅ Funcionamiento de DuckDuckGo
- ✅ Investigación completa end-to-end

### Prueba Manual

```python
import asyncio
from open_deep_research.deep_researcher import deep_researcher

async def test_research():
    config = {
        "configurable": {
            "research_model": "openai:http://localhost:1234/v1",
            "summarization_model": "openai:http://localhost:1234/v1",
            "compression_model": "openai:http://localhost:1234/v1",
            "final_report_model": "openai:http://localhost:1234/v1",
            "search_api": "duckduckgo",
            "max_concurrent_research_units": 3,
            "max_researcher_iterations": 4,
            "max_react_tool_calls": 8,
            "max_structured_output_retries": 3,
            "max_content_length": 50000,
            "allow_clarification": True
        }
    }
    
    result = await deep_researcher.ainvoke(
        {"messages": [{"role": "user", "content": "¿Cuáles son las últimas noticias sobre IA?"}]},
        config=config
    )
    
    print(result["final_report"])

# Ejecutar
asyncio.run(test_research())
```

## 🔧 Personalización

### Cambiar Modelo Local

Edita `config_local.env`:

```env
# Cambiar a otro modelo
RESEARCH_MODEL=openai:http://localhost:1234/v1
# El modelo real se especifica en la URL de tu API local
```

### Ajustar Parámetros de Investigación

```env
# Más unidades de investigación concurrentes (más rápido, más recursos)
MAX_CONCURRENT_RESEARCH_UNITS=5

# Más iteraciones de investigación (más profundo)
MAX_RESEARCHER_ITERATIONS=6

# Más llamadas de herramientas por iteración
MAX_REACT_TOOL_CALLS=10
```

### Cambiar Motor de Búsqueda

```env
# Usar Tavily (requiere API key)
SEARCH_API=tavily

# Usar búsqueda nativa de OpenAI
SEARCH_API=openai

# Usar búsqueda nativa de Anthropic
SEARCH_API=anthropic

# Sin búsqueda (solo modelo local)
SEARCH_API=none
```

## 🐛 Solución de Problemas

### Error: "Authorization header missing"

**Problema**: El servidor requiere autenticación.

**Solución**: Usa el script con autenticación local:
```bash
./start_local_dev.sh
```

### Error: "Incorrect API key provided"

**Problema**: Tu API local rechaza la clave API.

**Solución**: Verifica que tu API local no requiera autenticación:
```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": "test"}]}'
```

### Error: "No tools found to conduct research"

**Problema**: DuckDuckGo no está configurado correctamente.

**Solución**: Verifica la configuración:
```env
SEARCH_API=duckduckgo
```

### Error: "Connection refused"

**Problema**: LM Studio no está ejecutándose.

**Solución**: 
1. Abre LM Studio
2. Carga un modelo
3. Inicia el servidor en puerto 1234

## 📊 Rendimiento

### Recursos del Sistema

- **RAM**: ~12-15 GB (dependiendo del modelo)
- **GPU**: Recomendado para modelos grandes
- **CPU**: Mínimo 8 cores para buen rendimiento

### Optimizaciones

```env
# Reducir concurrencia para sistemas con menos recursos
MAX_CONCURRENT_RESEARCH_UNITS=2

# Reducir tokens para ahorrar memoria
RESEARCH_MODEL_MAX_TOKENS=5000
SUMMARIZATION_MODEL_MAX_TOKENS=4000
```

## 🔒 Seguridad

### Desarrollo Local

- ✅ No se envían datos a servicios externos
- ✅ Búsquedas a través de DuckDuckGo (sin tracking)
- ✅ Modelo ejecutándose localmente

### Producción

Para uso en producción, considera:
- Configurar autenticación real
- Usar HTTPS
- Implementar rate limiting
- Monitoreo de logs

## 📚 Ejemplos de Uso

### Investigación de Noticias

```python
pregunta = "¿Cuáles son las últimas noticias sobre inteligencia artificial en 2024?"
```

### Análisis de Mercado

```python
pregunta = "¿Cuál es el estado actual del mercado de criptomonedas?"
```

### Investigación Científica

```python
pregunta = "¿Cuáles son los últimos avances en computación cuántica?"
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [LangChain](https://langchain.com/) - Framework de IA
- [LangGraph](https://langchain.com/langgraph) - Grafo de agentes
- [LM Studio](https://lmstudio.ai/) - Servidor local de modelos
- [DuckDuckGo](https://duckduckgo.com/) - Motor de búsqueda privado

---

**¡Disfruta investigando con tu propio sistema de IA local!** 🚀

---

# 🔬 Open Deep Research (Documentación Original)

<img width="1388" height="298" alt="full_diagram" src="https://github.com/user-attachments/assets/12a2371b-8be2-4219-9b48-90503eb43c69" />

Deep research has broken out as one of the most popular agent applications. This is a simple, configurable, fully open source deep research agent that works across many model providers, search tools, and MCP servers. It's performance is on par with many popular deep research agents ([see Deep Research Bench leaderboard](https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard)).

<img width="817" height="666" alt="Screenshot 2025-07-13 at 11 21 12 PM" src="https://github.com/user-attachments/assets/052f2ed3-c664-4a4f-8ec2-074349dcaa3f" />

### 🔥 Recent Updates

**August 14, 2025**: See our free course [here](https://academy.langchain.com/courses/deep-research-with-langgraph) (and course repo [here](https://github.com/langchain-ai/deep_research_from_scratch)) on building open deep research.

**August 7, 2025**: Added GPT-5 and updated the Deep Research Bench evaluation w/ GPT-5 results.

**August 2, 2025**: Achieved #6 ranking on the [Deep Research Bench Leaderboard](https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard) with an overall score of 0.4344. 

**July 30, 2025**: Read about the evolution from our original implementations to the current version in our [blog post](https://rlancemartin.github.io/2025/07/30/bitter_lesson/).

**July 16, 2025**: Read more in our [blog](https://blog.langchain.com/open-deep-research/) and watch our [video](https://www.youtube.com/watch?v=agGiWUpxkhg) for a quick overview.

### 🚀 Quickstart

1. Clone the repository and activate a virtual environment:
```bash
git clone https://github.com/langchain-ai/open_deep_research.git
cd open_deep_research
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv sync
# or
uv pip install -r pyproject.toml
```

3. Set up your `.env` file to customize the environment variables (for model selection, search tools, and other configuration settings):
```bash
cp .env.example .env
```

4. Launch agent with the LangGraph server locally:

```bash
# Install dependencies and start the LangGraph server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

This will open the LangGraph Studio UI in your browser.

```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

Ask a question in the `messages` input field and click `Submit`. Select different configuration in the "Manage Assistants" tab.

### ⚙️ Configurations

#### LLM :brain:

Open Deep Research supports a wide range of LLM providers via the [init_chat_model() API](https://python.langchain.com/docs/how_to/chat_models_universal_init/). It uses LLMs for a few different tasks. See the below model fields in the [configuration.py](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py) file for more details. This can be accessed via the LangGraph Studio UI. 

- **Summarization** (default: `openai:gpt-4.1-mini`): Summarizes search API results
- **Research** (default: `openai:gpt-4.1`): Power the search agent
- **Compression** (default: `openai:gpt-4.1`): Compresses research findings
- **Final Report Model** (default: `openai:gpt-4.1`): Write the final report

> Note: the selected model will need to support [structured outputs](https://python.langchain.com/docs/integrations/chat/) and [tool calling](https://python.langchain.com/docs/how_to/tool_calling/).

> Note: For OpenRouter: Follow [this guide](https://github.com/langchain-ai/open_deep_research/issues/75#issuecomment-2811472408) and for local models via Ollama  see [setup instructions](https://github.com/langchain-ai/open_deep_research/issues/65#issuecomment-2743586318).

#### Search API :mag:

Open Deep Research supports a wide range of search tools. By default it uses the [Tavily](https://www.tavily.com/) search API. Has full MCP compatibility and work native web search for Anthropic and OpenAI. See the `search_api` and `mcp_config` fields in the [configuration.py](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py) file for more details. This can be accessed via the LangGraph Studio UI. 

#### Other 

See the fields in the [configuration.py](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py) for various other settings to customize the behavior of Open Deep Research. 

### 📊 Evaluation

Open Deep Research is configured for evaluation with [Deep Research Bench](https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard). This benchmark has 100 PhD-level research tasks (50 English, 50 Chinese), crafted by domain experts across 22 fields (e.g., Science & Tech, Business & Finance) to mirror real-world deep-research needs. It has 2 evaluation metrics, but the leaderboard is based on the RACE score. This uses LLM-as-a-judge (Gemini) to evaluate research reports against a golden set of reports compiled by experts across a set of metrics.

#### Usage

> Warning: Running across the 100 examples can cost ~$20-$100 depending on the model selection.

The dataset is available on [LangSmith via this link](https://smith.langchain.com/public/c5e7a6ad-fdba-478c-88e6-3a388459ce8b/d). To kick off evaluation, run the following command:

```bash
# Run comprehensive evaluation on LangSmith datasets
python tests/run_evaluate.py
```

This will provide a link to a LangSmith experiment, which will have a name `YOUR_EXPERIMENT_NAME`. Once this is done, extract the results to a JSONL file that can be submitted to the Deep Research Bench.

```bash
python tests/extract_langsmith_data.py --project-name "YOUR_EXPERIMENT_NAME" --model-name "you-model-name" --dataset-name "deep_research_bench"
```

This creates `tests/expt_results/deep_research_bench_model-name.jsonl` with the required format. Move the generated JSONL file to a local clone of the Deep Research Bench repository and follow their [Quick Start guide](https://github.com/Ayanami0730/deep_research_bench?tab=readme-ov-file#quick-start) for evaluation submission.

#### Results 

| Name | Commit | Summarization | Research | Compression | Total Cost | Total Tokens | RACE Score | Experiment |
|------|--------|---------------|----------|-------------|------------|--------------|------------|------------|
| GPT-5 | [ca3951d](https://github.com/langchain-ai/open_deep_research/pull/168/commits) | openai:gpt-4.1-mini | openai:gpt-5 | openai:gpt-4.1 |  | 204,640,896 | 0.4943 | [Link](https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/datasets/6e4766ca-613c-4bda-8bde-f64f0422bbf3/compare?selectedSessions=4d5941c8-69ce-4f3d-8b3e-e3c99dfbd4cc&baseline=undefined) |
| Defaults | [6532a41](https://github.com/langchain-ai/open_deep_research/commit/6532a4176a93cc9bb2102b3d825dcefa560c85d9) | openai:gpt-4.1-mini | openai:gpt-4.1 | openai:gpt-4.1 | $45.98 | 58,015,332 | 0.4309 | [Link](https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/datasets/6e4766ca-6[…]ons=cf4355d7-6347-47e2-a774-484f290e79bc&baseline=undefined) |
| Claude Sonnet 4 | [f877ea9](https://github.com/langchain-ai/open_deep_research/pull/163/commits/f877ea93641680879c420ea991e998b47aab9bcc) | openai:gpt-4.1-mini | anthropic:claude-sonnet-4-20250514 | openai:gpt-4.1 | $187.09 | 138,917,050 | 0.4401 | [Link](https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/datasets/6e4766ca-6[…]ons=04f6002d-6080-4759-bcf5-9a52e57449ea&baseline=undefined) |
| Deep Research Bench Submission | [c0a160b](https://github.com/langchain-ai/open_deep_research/commit/c0a160b57a9b5ecd4b8217c3811a14d8eff97f72) | openai:gpt-4.1-nano | openai:gpt-4.1 | openai:gpt-4.1 | $87.83 | 207,005,549 | 0.4344 | [Link](https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/datasets/6e4766ca-6[…]ons=e6647f74-ad2f-4cb9-887e-acb38b5f73c0&baseline=undefined) |

### 🚀 Deployments and Usage

#### LangGraph Studio

Follow the [quickstart](#-quickstart) to start LangGraph server locally and test the agent out on LangGraph Studio.

#### Hosted deployment
 
You can easily deploy to [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/#deployment-options). 

#### Open Agent Platform

Open Agent Platform (OAP) is a UI from which non-technical users can build and configure their own agents. OAP is great for allowing users to configure the Deep Researcher with different MCP tools and search APIs that are best suited to their needs and the problems that they want to solve.

We've deployed Open Deep Research to our public demo instance of OAP. All you need to do is add your API Keys, and you can test out the Deep Researcher for yourself! Try it out [here](https://oap.langchain.com)

You can also deploy your own instance of OAP, and make your own custom agents (like Deep Researcher) available on it to your users.
1. [Deploy Open Agent Platform](https://docs.oap.langchain.com/quickstart)
2. [Add Deep Researcher to OAP](https://docs.oap.langchain.com/setup/agents)

### Legacy Implementations 🏛️

The `src/legacy/` folder contains two earlier implementations that provide alternative approaches to automated research. They are less performant than the current implementation, but provide alternative ideas understanding the different approaches to deep research.

#### 1. Workflow Implementation (`legacy/graph.py`)
- **Plan-and-Execute**: Structured workflow with human-in-the-loop planning
- **Sequential Processing**: Creates sections one by one with reflection
- **Interactive Control**: Allows feedback and approval of report plans
- **Quality Focused**: Emphasizes accuracy through iterative refinement

#### 2. Multi-Agent Implementation (`legacy/multi_agent.py`)  
- **Supervisor-Researcher Architecture**: Coordinated multi-agent system
- **Parallel Processing**: Multiple researchers work simultaneously
- **Speed Optimized**: Faster report generation through concurrency
- **MCP Support**: Extensive Model Context Protocol integration