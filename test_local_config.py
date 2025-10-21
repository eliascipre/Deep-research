#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del Deep Research con API local y DuckDuckGo.
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from open_deep_research.deep_researcher import deep_researcher
from open_deep_research.configuration import Configuration

async def test_local_configuration():
    """Prueba la configuración local del Deep Research."""
    
    print("🔧 Probando configuración del Deep Research con API local y DuckDuckGo...")
    
    # Cargar variables de entorno desde el archivo de configuración
    env_file = Path(__file__).parent / "config_local.env"
    if env_file.exists():
        print(f"📁 Cargando configuración desde: {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        # Solo establecer la variable si tiene un valor no vacío
                        if value.strip():
                            os.environ[key] = value
    else:
        print("⚠️  Archivo de configuración no encontrado, usando variables de entorno por defecto")
    
    # Configuración para la prueba
    config = {
        "configurable": {
            "research_model": os.getenv("RESEARCH_MODEL", "openai:http://localhost:1234/v1"),
            "summarization_model": os.getenv("SUMMARIZATION_MODEL", "openai:http://localhost:1234/v1"),
            "compression_model": os.getenv("COMPRESSION_MODEL", "openai:http://localhost:1234/v1"),
            "final_report_model": os.getenv("FINAL_REPORT_MODEL", "openai:http://localhost:1234/v1"),
            "search_api": os.getenv("SEARCH_API", "duckduckgo"),
            "research_model_max_tokens": int(os.getenv("RESEARCH_MODEL_MAX_TOKENS", "10000")),
            "summarization_model_max_tokens": int(os.getenv("SUMMARIZATION_MODEL_MAX_TOKENS", "8192")),
            "compression_model_max_tokens": int(os.getenv("COMPRESSION_MODEL_MAX_TOKENS", "8192")),
            "final_report_model_max_tokens": int(os.getenv("FINAL_REPORT_MODEL_MAX_TOKENS", "10000")),
            "max_concurrent_research_units": int(os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", "3")),
            "max_researcher_iterations": int(os.getenv("MAX_RESEARCHER_ITERATIONS", "4")),
            "max_react_tool_calls": int(os.getenv("MAX_REACT_TOOL_CALLS", "8")),
            "max_structured_output_retries": int(os.getenv("MAX_STRUCTURED_OUTPUT_RETRIES", "3")),
            "max_content_length": int(os.getenv("MAX_CONTENT_LENGTH", "50000")),
            "allow_clarification": os.getenv("ALLOW_CLARIFICATION", "true").lower() == "true"
        }
    }
    
    # Agregar configuración de API keys solo si están definidas
    api_keys = {}
    if os.getenv("OPENAI_API_KEY"):
        api_keys["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    if os.getenv("ANTHROPIC_API_KEY"):
        api_keys["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
    if os.getenv("GOOGLE_API_KEY"):
        api_keys["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    
    if api_keys:
        config["configurable"]["apiKeys"] = api_keys
    
    # Verificar configuración
    print("\n📋 Configuración cargada:")
    print(f"  - Modelo de investigación: {config['configurable']['research_model']}")
    print(f"  - Modelo de resumen: {config['configurable']['summarization_model']}")
    print(f"  - API de búsqueda: {config['configurable']['search_api']}")
    print(f"  - Unidades de investigación concurrentes: {config['configurable']['max_concurrent_research_units']}")
    
    # Pregunta de prueba simple
    test_question = "¿Cuáles son las últimas noticias sobre inteligencia artificial en 2024?"
    
    print(f"\n🔍 Pregunta de prueba: {test_question}")
    print("\n⏳ Iniciando investigación...")
    
    try:
        # Ejecutar el deep research
        result = await deep_researcher.ainvoke(
            {"messages": [{"role": "user", "content": test_question}]},
            config=config
        )
        
        print("\n✅ Investigación completada exitosamente!")
        print("\n📄 Resultado:")
        print("=" * 80)
        
        # Mostrar el resultado final
        if "final_report" in result:
            print(result["final_report"])
        elif "messages" in result and result["messages"]:
            print(result["messages"][-1].content if hasattr(result["messages"][-1], 'content') else str(result["messages"][-1]))
        else:
            print("No se pudo obtener el resultado final")
            
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error durante la investigación: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        
        # Sugerencias de solución
        print("\n💡 Posibles soluciones:")
        print("1. Verifica que tu API local esté ejecutándose en localhost:1234")
        print("2. Asegúrate de que el endpoint /v1/chat/completions esté disponible")
        print("3. Verifica que el modelo 'openai/gpt-oss-20b' esté disponible en tu API")
        print("4. Revisa los logs de tu API local para más detalles")
        
        return False
    
    return True

async def test_duckduckgo_search():
    """Prueba la funcionalidad de búsqueda DuckDuckGo."""
    
    print("\n🔍 Probando búsqueda DuckDuckGo...")
    
    try:
        from open_deep_research.utils import duckduckgo_search_async
        
        # Prueba de búsqueda simple
        results = await duckduckgo_search_async(["inteligencia artificial"], max_results=3)
        
        print("✅ Búsqueda DuckDuckGo funcionando correctamente!")
        print(f"📊 Resultados encontrados: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"\nResultado {i+1}:")
            print(f"  Query: {result['query']}")
            print(f"  Resultados: {len(result['results'])}")
            if result['results']:
                print(f"  Primer resultado: {result['results'][0]['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en búsqueda DuckDuckGo: {str(e)}")
        return False

def test_api_connection():
    """Prueba la conexión a la API local."""
    
    print("\n🌐 Probando conexión a API local...")
    
    try:
        import requests
        
        # URL de tu API local
        api_url = "http://localhost:1234/v1/chat/completions"
        
        # Datos de prueba basados en tu curl
        test_data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
                {"role": "user", "content": "What day is it today?"}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        
        response = requests.post(api_url, json=test_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión a API local exitosa!")
            result = response.json()
            if 'choices' in result and result['choices']:
                print(f"📝 Respuesta de prueba: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ Error en API local: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar a localhost:1234")
        print("💡 Asegúrate de que tu API local esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

async def main():
    """Función principal de prueba."""
    
    print("🚀 Iniciando pruebas del Deep Research con configuración local")
    print("=" * 80)
    
    # Prueba 1: Conexión a API local
    api_ok = test_api_connection()
    
    # Prueba 2: Búsqueda DuckDuckGo
    search_ok = await test_duckduckgo_search()
    
    # Prueba 3: Deep Research completo (solo si las anteriores pasan)
    if api_ok and search_ok:
        print("\n" + "=" * 80)
        research_ok = await test_local_configuration()
        
        if research_ok:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            print("✅ Tu configuración local está lista para usar")
        else:
            print("\n⚠️  Algunas pruebas fallaron, pero la configuración básica funciona")
    else:
        print("\n❌ Pruebas básicas fallaron. Revisa la configuración antes de continuar.")
    
    print("\n" + "=" * 80)
    print("📚 Para usar el Deep Research:")
    print("1. Asegúrate de que tu API local esté ejecutándose en localhost:1234")
    print("2. Ejecuta: uvx --refresh --from 'langgraph-cli[inmem]' --with-editable . --python 3.11 langgraph dev --allow-blocking")
    print("3. Abre http://127.0.0.1:2024 en tu navegador")
    print("4. Configura el Search API como 'DuckDuckGo' en la interfaz")

if __name__ == "__main__":
    asyncio.run(main())
