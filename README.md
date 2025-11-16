# Backend WhatsApp + Flask + IA

Sistema backend integrado ao WhatsApp que processa áudios, vídeos e textos usando inteligência artificial.

## 🚀 Funcionalidades

- **Webhook WhatsApp**: Recebe mensagens via Z-Api
- **Processamento de Áudio**: Transcrição com Whisper + resposta via GPT/Gemini
- **Análise de Vídeo**: Relatórios de performance esportiva com Gemini
- **Síntese de Voz**: Respostas em áudio via ElevenLabs
- **Banco de Dados**: SQLite para usuários e mensagens
- **Sistema de Autorização**: Controle de usuários autorizados

## 📦 Instalação

```bash
# 1. Entre na pasta do backend
cd backend

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# 4. Execute o servidor
python main.py
```

## 🔧 Configuração

### 1. Z-Api (WhatsApp)
- Crie uma conta na [Z-Api](https://z-api.io)
- Configure sua instância do WhatsApp
- Adicione as credenciais no `.env`

### 2. OpenAI (Whisper + GPT)
- Obtenha sua API key da [OpenAI](https://platform.openai.com)
- Adicione no `.env`

### 3. Google Gemini
- Configure no [Google AI Studio](https://makersuite.google.com)
- Adicione a API key no `.env`

### 4. ElevenLabs (Síntese de Voz)
- Crie conta na [ElevenLabs](https://elevenlabs.io)
- Configure voz e obtenha as credenciais

### 5. Usuários Autorizados
- Adicione os números de telefone autorizados no `.env`
- Formato: `5511999999999,5511888888888`

## 🌐 Endpoints

- `GET /` - Health check
- `GET /health` - Status da aplicação
- `POST /api/webhook/zapi` - Webhook do Z-Api
- `GET /api/webhook/status` - Status do webhook

## 🔄 Fluxo de Funcionamento

1. **Mensagem Recebida** → Webhook processa
2. **Verificação** → Usuário autorizado?
3. **Processamento**:
   - **Áudio** → Whisper transcreve → GPT responde
   - **Vídeo** → Gemini analisa → Relatório de performance
   - **Texto** → GPT/Gemini responde
4. **Resposta** → Enviada via Z-Api
5. **Log** → Salvo no banco de dados

## 📁 Estrutura

```
backend/
├── main.py              # Aplicação Flask principal
├── config/settings.py   # Configurações e variáveis
├── routes/             # Rotas da API
├── services/           # Lógica de negócio
├── clients/            # Integrações externas
├── db/                 # Banco de dados
├── core/               # Utilitários
└── logs/               # Arquivos de log
```

## 🧪 Teste

```bash
# Teste básico da API
curl http://localhost:5000/health

# Simular webhook (substitua pelos dados reais)
curl -X POST http://localhost:5000/api/webhook/zapi \
  -H "Content-Type: application/json" \
  -d '{"phone":"5511999999999","type":"text","body":{"message":"Oi"}}'
```

## 📝 Próximos Passos

- [ ] Implementar upload de arquivos para cloud
- [ ] Melhorar sistema de contexto das conversas
- [ ] Adicionar métricas e monitoramento
- [ ] Implementar rate limiting
- [ ] Adicionar testes automatizados
- [ ] Deploy em produção

## ⚠️ Importante

- Configure corretamente o `.env` antes de executar
- Mantenha as API keys seguras
- Teste primeiro com números autorizados
- Monitor os logs em `backend/logs/`

## 🆘 Suporte

Em caso de dúvidas, verifique:
1. Configuração do `.env`
2. Logs da aplicação
3. Status das APIs externas
4. Conexão com WhatsApp (Z-Api)