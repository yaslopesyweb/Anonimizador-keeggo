@echo off
REM Setup script para Anonimizador - Windows
REM Este script configura o ambiente e instala dependências

echo =========================================
echo Setup - Anonimizador Keeggo
echo =========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo. ❌ Python não encontrado. Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% encontrado
echo.

REM Criar ambiente virtual
echo 📦 Criando ambiente virtual...
if not exist ".venv" (
    python -m venv .venv
    echo ✓ Ambiente virtual criado
) else (
    echo ✓ Ambiente virtual já existe
)

REM Ativar ambiente virtual
echo.
echo 🔌 Ativando ambiente virtual...
call .venv\Scripts\activate.bat
echo ✓ Ambiente virtual ativado

REM Atualizar pip
echo.
echo 🔧 Atualizando pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo ✓ pip atualizado

REM Instalar dependências Python
echo.
echo 📚 Instalando dependências Python...
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependências instaladas

REM Baixar modelo spaCy
echo.
echo 🧠 Baixando modelo de linguagem spaCy (pt_core_news_lg)...
echo    (Isto pode levar alguns minutos na primeira vez...)
python -m spacy download pt_core_news_lg
echo ✓ Modelo spaCy baixado

echo.
echo =========================================
echo ✅ Setup concluído com sucesso!
echo =========================================
echo.
echo Para iniciar a aplicação, execute:
echo.
echo   .venv\Scripts\activate.bat
echo   streamlit run anonimizador_streamlit.py
echo.
echo A aplicação abrirá em: http://localhost:8501
echo.
pause
