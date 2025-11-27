# Script PowerShell para testar webhook Z-API
# Uso: .\test_webhook.ps1

$WEBHOOK_URL = "http://localhost:8000/whatsapp/receive_whatsapp_message"

Write-Host ""
Write-Host "Testando webhook Z-API - Mensagem de Texto" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$body = @{
    phone = "5511999999999"
    message_id = "test-msg-123"
    text = @{
        message = "Ola! Quanto gastei hoje?"
    }
} | ConvertTo-Json

Write-Host "Enviando requisicao..." -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $WEBHOOK_URL -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Resposta recebida:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "Erro ao enviar requisicao:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Certifique-se que o servidor esta rodando: python main.py" -ForegroundColor Yellow
}

Write-Host "Teste concluido!" -ForegroundColor Green
Write-Host ""
