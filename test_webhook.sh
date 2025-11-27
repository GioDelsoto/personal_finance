#!/usr/bin/env bash

# Script para testar webhook simulando Z-API
# Uso: bash test_webhook.sh

WEBHOOK_URL="http://localhost:8000/whatsapp/receive_whatsapp_message"

echo ""
echo "🚀 Testando webhook Z-API - Mensagem de Texto"
echo "=============================================="
echo ""

curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5511999999999",
    "message_id": "test-msg-123",
    "text": {
      "message": "Olá! Quanto gastei hoje?"
    }
  }' \
  | jq

echo ""
echo "✅ Teste concluído!"
echo ""
