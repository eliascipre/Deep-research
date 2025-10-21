#!/bin/bash

# Script para iniciar Deep Research con configuración local sin autenticación

echo "🚀 Iniciando Deep Research con configuración local (sin autenticación)..."

# Verificar que el archivo de configuración existe
if [ ! -f "config_local.env" ]; then
    echo "❌ Archivo de configuración config_local.env no encontrado"
    echo "💡 Asegúrate de que el archivo existe en el directorio actual"
    exit 1
fi

# Cargar variables de entorno
echo "📁 Cargando configuración local..."
export $(grep -v '^#' config_local.env | xargs)

# Verificar que la API local esté ejecutándose
echo "🌐 Verificando conexión a API local..."
if curl -s http://localhost:1234/v1/chat/completions > /dev/null; then
    echo "✅ API local detectada en localhost:1234"
else
    echo "⚠️  No se pudo conectar a localhost:1234"
    echo "💡 Asegúrate de que tu API local esté ejecutándose antes de continuar"
    echo "   Puedes probar con: curl http://localhost:1234/v1/chat/completions"
    read -p "¿Continuar de todas formas? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
if ! python -c "import duckduckgo_search" 2>/dev/null; then
    echo "📥 Instalando duckduckgo-search..."
    pip install duckduckgo-search
fi

# Ejecutar el servidor LangGraph con autenticación local
echo "🎯 Iniciando servidor LangGraph con autenticación local..."
echo "📱 Una vez iniciado, abre http://127.0.0.1:2024 en tu navegador"
echo "⚙️  Configura el Search API como 'DuckDuckGo' en la interfaz"
echo "🔓 No se requiere autenticación para desarrollo local"
echo ""

# Usar la autenticación local en lugar de la de Supabase
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking --auth ./src/security/auth_local.py:auth
