@echo off
echo ========================================
echo Helper - Script de Instalacao
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.9+ de https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Criando ambiente virtual...
if exist venv (
    echo Ambiente virtual ja existe, pulando...
) else (
    python -m venv venv
    echo Ambiente virtual criado!
)
echo.

echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.

echo [4/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/5] Configurando arquivo .env...
if exist config\.env (
    echo Arquivo .env ja existe, pulando...
) else (
    copy config\.env.example config\.env
    echo Arquivo .env criado!
    echo IMPORTANTE: Edite config\.env com suas credenciais
)
echo.

echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Proximos passos:
echo 1. Edite config\.env com suas credenciais
echo 2. Coloque google_credentials.json em config\
echo 3. Execute iniciar_backend.bat para testar
echo.
echo Consulte docs\INSTALACAO.md para mais detalhes
echo.
pause

@REM Made with Bob
