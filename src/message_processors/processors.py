from .interface_processors import MessageProcessor
from src.schemas.messages.received_messages import ReceivedMessage
from src.schemas.messages.chat_messages import ChatMessage
from openai import OpenAI
from typing import List
import json
from datetime import datetime
from src.dependencies.llm_client import get_openai_client

class NormalChatProcessor(MessageProcessor):
    def __init__(self):

        self.client = get_openai_client()
        print("client em runtime ->", type(self.client))

    def _prepare_chat_history(self, chat_history: List[ChatMessage]) -> List[dict]:
        """Converts chat history to OpenAI format"""
        return [
            {"role": msg.role, "content": msg.content} 
            for msg in chat_history
        ]
    
    def _get_system_prompt(self) -> str:
        """Returns the system prompt for normal chat interactions"""
        return """Você é um assistente financeiro prestativo que ajuda usuários a gerenciar suas finanças pessoais, rastrear despesas e fornecer conselhos sobre orçamento. Sempre responda em português."""


    def process_message(self, message: ReceivedMessage, chat_history: List[ChatMessage], user: dict) -> dict:
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        messages.extend(self._prepare_chat_history(chat_history))
        messages.append({"role": "user", "content": message.text})
        
        try:   
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return {
                "response": response.choices[0].message.content, 
                "status": "success"
            }

        except Exception as e:
            return {
                "response": f"Error: {str(e)}", 
                "status": "error"
            }


class AddExpenseProcessor(MessageProcessor):
    def __init__(self):
        self.client = get_openai_client()
    
    def _prepare_chat_history(self, chat_history: List[ChatMessage]) -> List[dict]:
        """Converte histórico de chat para formato OpenAI"""
        return [
            {"role": msg.role, "content": msg.content} 
            for msg in chat_history
        ]
    
    def _get_system_prompt(self) -> str:
        """Retorna o system prompt para extração de despesas"""
        today = datetime.today().strftime("%Y-%m-%d")
        return f"""Você é um assistente financeiro que extrai detalhes de despesas das mensagens do usuário.

        REGRAS:
        1. Retorne APENAS um objeto JSON válido com esta estrutura exata:
        {{
            "expense_data": {{
                "amount": float,
                "category": string,
                "date": "YYYY-MM-DD",
                "description": string
            }},
            "clarification_message": string
        }}

        2. Categorias permitidas: alimentacao, transporte, entretenimento, contas, saude, outros
        3. A data de hoje é {today} - use como padrão se nenhuma data for fornecida
        4. Se informações estiverem faltando ou não estiverem claras, defina clarification_message com uma pergunta
        5. Se tudo estiver claro, defina clarification_message como string vazia ""
        6. Use o histórico da conversa para contexto (usuário pode se referir a mensagens anteriores)
        7. Sempre responda em português

        EXEMPLOS:
        Usuário: "Gastei 50 reais no almoço"
        Resposta: {{"expense_data": {{"amount": 50.0, "category": "alimentacao", "date": "{today}", "description": "almoço"}}, "clarification_message": ""}}

        Usuário: "Comprei algo por 100"
        Resposta: {{"expense_data": {{"amount": 100.0, "category": "outros", "date": "{today}", "description": "compra"}}, "clarification_message": "Em qual categoria essa despesa se encaixa? (alimentacao, transporte, entretenimento, contas, saude, outros)"}}
        """

            
    def process_message(self, message: ReceivedMessage, chat_history: List[ChatMessage], user: dict) -> dict:
        # Monta as mensagens com histórico + system prompt + mensagem atual
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        messages.extend(self._prepare_chat_history(chat_history))
        messages.append({"role": "user", "content": message.text})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=500,
                temperature=0  # Mais determinístico
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if not result.get("clarification_message"):
                if self._save_expense_to_db(result["expense_data"], user):
                    return {
                        "status": "expense_added",
                        "response": f"Despesa adicionada: R$ {result['expense_data']['amount']:.2f} - {result['expense_data']['category']}",
                    }
                else:
                    return {
                        "status": "error",
                        "response": "Erro ao salvar a despesa. Por favor, tente novamente.",
                    }
            else:
                # Precisa de mais informações
                return {
                    "status": "clarification_needed",
                    "response": result["clarification_message"],
                }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "response": "Erro ao processar a despesa. Por favor, tente novamente."
            }
        except Exception as e:
            return {
                "status": "error",
                "response": f"Error while processing message in processors.py: {str(e)}"
            }
    
    def _save_expense_to_db(self, expense_data: dict, user: dict):
        """Salva despesa no banco de dados"""
        # TODO: Implementar lógica de salvamento
        # - Conectar ao PostgreSQL
        # - Inserir expense_data com user_id
        # - Validar dados antes de salvar
        return True