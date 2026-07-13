@echo off
cd /d "%~dp0"

echo ================================================
echo   Sistema de Encomendas do Condominio
echo ================================================
echo.

REM Verifica se o Python esta disponivel
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Por favor instale o Python 3.12 ou superior em https://python.org
    echo E marque a opcao "Add python.exe to PATH" durante a instalacao.
    pause
    exit /b
)

REM Cria o venv se nao existir
if not exist "venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Falha ao criar o ambiente virtual.
        pause
        exit /b
    )
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependencias se necessario
if not exist "venv\Lib\site-packages\flask" (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando o sistema...
echo Acesse no navegador: http://127.0.0.1:5000
echo.
python app.py

pause
