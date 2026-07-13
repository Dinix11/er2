<<<<<<< HEAD
@echo off
chcp 65001 >nul
echo ============================================================
echo  INSTALADOR DO SISTEMA DE ENCOMENDAS - CLOUDFLARE R2
echo ============================================================
echo.

REM Verifica Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.12 ou superior em:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marque a opcao "Add Python to PATH" durante a instalacao!
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado!
echo.

REM Cria ambiente virtual
echo [2/4] Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    echo ✅ Ambiente virtual criado!
) else (
    echo ⚠️  Ambiente virtual ja existe!
)
echo.

REM Ativa ambiente virtual
echo [3/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo ✅ Ambiente virtual ativado!
echo.

REM Instala dependências
echo [4/4] Instalando dependencias...
pip install -r requirements.txt --quiet
echo.
echo ✅ Dependencias instaladas!
echo.

REM Cria arquivo .env se não existir
if not exist ".env" (
    echo Criando arquivo .env...
    copy .env.example .env >nul
    echo ⚠️  Arquivo .env criado!
    echo.
    echo IMPORTANTE: Edite o arquivo .env e adicione suas credenciais do Cloudflare R2
    echo.
)

echo ============================================================
echo  INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas credenciais do Cloudflare R2
echo 2. Execute: python test_r2.py (para testar a conexao)
echo 3. Execute: python app.py (para iniciar o sistema)
echo.
echo Acesse: http://127.0.0.1:5000
echo.
=======
@echo off
chcp 65001 >nul
echo ============================================================
echo  INSTALADOR DO SISTEMA DE ENCOMENDAS - CLOUDFLARE R2
echo ============================================================
echo.

REM Verifica Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.12 ou superior em:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marque a opcao "Add Python to PATH" durante a instalacao!
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado!
echo.

REM Cria ambiente virtual
echo [2/4] Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    echo ✅ Ambiente virtual criado!
) else (
    echo ⚠️  Ambiente virtual ja existe!
)
echo.

REM Ativa ambiente virtual
echo [3/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo ✅ Ambiente virtual ativado!
echo.

REM Instala dependências
echo [4/4] Instalando dependencias...
pip install -r requirements.txt --quiet
echo.
echo ✅ Dependencias instaladas!
echo.

REM Cria arquivo .env se não existir
if not exist ".env" (
    echo Criando arquivo .env...
    copy .env.example .env >nul
    echo ⚠️  Arquivo .env criado!
    echo.
    echo IMPORTANTE: Edite o arquivo .env e adicione suas credenciais do Cloudflare R2
    echo.
)

echo ============================================================
echo  INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas credenciais do Cloudflare R2
echo 2. Execute: python test_r2.py (para testar a conexao)
echo 3. Execute: python app.py (para iniciar o sistema)
echo.
echo Acesse: http://127.0.0.1:5000
echo.
>>>>>>> 160b0632a2e300896dbc7978624f212684350ef0
pause