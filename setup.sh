#!/bin/bash
# Setup script para Anonimizador - Linux/macOS
# Este script configura o ambiente e instala dependências

set -e

echo "========================================="
echo "Setup - Anonimizador Keeggo"
echo "========================================="
echo ""

# Verificar se Python 3.8+ está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION encontrado"
echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Ambiente virtual criado"
else
    echo "✓ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo ""
echo "🔌 Ativando ambiente virtual..."
source .venv/bin/activate
echo "✓ Ambiente virtual ativado"

# Atualizar pip
echo ""
echo "🔧 Atualizando pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip atualizado"

# Instalar dependências Python
echo ""
echo "📚 Instalando dependências Python..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependências instaladas"

# Baixar modelo spaCy
echo ""
echo "🧠 Baixando modelo de linguagem spaCy (pt_core_news_lg)..."
echo "   (Isto pode levar alguns minutos na primeira vez...)"
python -m spacy download pt_core_news_lg
echo "✓ Modelo spaCy baixado"

echo ""
echo "========================================="
echo "✅ Setup concluído com sucesso!"
echo "========================================="
echo ""
echo "Para iniciar a aplicação, execute:"
echo ""
echo "  source .venv/bin/activate"
echo "  streamlit run anonimizador_streamlit.py"
echo ""
echo "A aplicação abrirá em: http://localhost:8501"
echo ""
