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
