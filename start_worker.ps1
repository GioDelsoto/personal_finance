# Script para iniciar Celery Worker
# Uso: .\start_worker.ps1

Write-Host ""
Write-Host "Iniciando Celery Worker..." -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

# Ativa o virtual environment
& ".\venv\Scripts\Activate.ps1"

# Inicia o worker
Write-Host "Worker rodando - Pressione Ctrl+C para parar" -ForegroundColor Green
Write-Host ""

celery -A src.celery_app worker --loglevel=info --pool=solo
