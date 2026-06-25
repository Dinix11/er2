# Script para executar o Sistema de Encomendas
# Rode com: .\run.ps1

Set-Location $PSScriptRoot

Write-Host "Iniciando Sistema de Encomendas do Condomínio..." -ForegroundColor Cyan
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow

& ".\venv\Scripts\Activate.ps1"

Write-Host "`nServidor iniciando em http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Pressione CTRL+C para parar.`n" -ForegroundColor Gray

python app.py
