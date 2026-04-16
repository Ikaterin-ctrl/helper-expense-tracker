@echo off
echo ========================================
echo Helper - Iniciando Widget Windows
echo ========================================
echo.

cd /d "%~dp0"

REM Ativa ambiente virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute: python -m venv venv
    pause
    exit /b 1
)

REM Verifica se .env existe
if not exist config\.env (
    echo ERRO: Arquivo config\.env nao encontrado!
    echo Copie config\.env.example para config\.env e configure
    pause
    exit /b 1
)

echo Iniciando widget...
echo.

REM Usa pythonw para nao mostrar console
start pythonw widget\helper_ui.pyw

echo Widget iniciado!
timeout /t 2 >nul

@REM Made with Bob
