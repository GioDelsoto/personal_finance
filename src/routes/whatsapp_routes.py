import sys
import os

from FastAPI import FastAPI, Request, APIRouter, HTTPException
from src.utils.phone_formatter import format_phone_number
import time
import logging

from src.middleware.authorization_service import AuthorizationService
from src.parsers.interface_received_message_adapter import InterfaceReceivedMessageAdapter


router = APIRouter()

@router.post("/receive_whatsapp_message")
async def receive_whatsapp_message(request: Request): 
    """Webhook para receber mensagens do WhatsApp"""
    try:
        data = request.json

        parser 

        #Authentication and Services Initialization

        #Session Management
        

        user = session['user']
        session_id = session['session_id']
        if not user:
            unauthorized_message = "You are not registered client. Access www.website.com to have access to your Elite Coach"
            zapi_client.send_message(phone, unauthorized_message)
            return jsonify({"status": "unauthorized", "message": "User not authorized"}), 200

        # Message type and extraction
        message_type, processing_data = MessageTypeHandler.detect_and_extract(data)
        processing_data['phone'] = phone  # Ensure phone is set

        # Process message
        start_time = time.time()
        response_text = message_processor.process(message_type, processing_data, user, session_id, 'whatsapp', db_client, redis_client)
        processing_time = time.time() - start_time

        # Send and save response
        success = response_sender.send_and_save(user, response_text, session_id, 'whatsapp')

        return jsonify({
            "status": "success",
            "sent": success,
            "message_id": processing_data.get('message_id', ''),
            "processing_time": f"{processing_time:.2f}s"
        }), 200

    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
