@echo off
chcp 65001 >nul
echo ========================================
echo  CONFIGURAR GITHUB - ENCOMENDAS R2
echo ========================================
echo.

REM Verificar se git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não encontrado!
    echo.
    echo Por favor, instale o Git em: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git encontrado
echo.

REM Solicitar informações do usuário
set /p github_user="Digite seu usuário do GitHub: "
set /p repo_name="Digite o nome do repositório (ex: encomendas-mirantes): "

echo.
echo ========================================
echo  CONFIGURANDO GIT...
echo ========================================
echo.

REM Inicializar git se não existir
if not exist .git (
    echo 📦 Inicializando repositório Git...
    git init
    echo ✅ Git inicializado
) else (
    echo ✅ Git já inicializado
)

echo.
echo 📝 Adicionando arquivos...
git add .

echo.
echo 💾 Fazendo commit...
git commit -m "Sistema de Encomendas R2 - Versão inicial"

echo.
echo 🔗 Conectando ao GitHub...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%github_user%/%repo_name%.git

echo.
echo 🌿 Criando branch main...
git branch -M main

echo.
echo ========================================
echo  PRONTO PARA ENVIAR!
echo ========================================
echo.
echo Agora execute:
echo   git push -u origin main
echo.
echo Ou se o repositório já existir no GitHub:
echo   git push -u origin main --force
echo.
pause