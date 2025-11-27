from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import ValidationError
from src.parsers.interface_received_message_adapter import InterfaceReceivedMessageAdapter
from src.dependencies.messages import get_message_parser, get_messages_controller
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/receive_whatsapp_message")
async def receive_whatsapp_message(
    request: Request,
    parser: InterfaceReceivedMessageAdapter = Depends(get_message_parser),
    controller = Depends(get_messages_controller)
):
    """Webhook para receber mensagens do WhatsApp"""
    try:
        # Recebe request raw
        data = await request.json()
        
        # Parser: transforma request em ReceivedMessage
        try:
            received_message = parser.parse_request(data)
        except ValidationError as e:
            logger.error(f"Validation error parsing request: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request format: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error parsing request: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse request: {str(e)}"
            )
        
        # Controller: processa mensagem
        result = controller.message_controller(received_message)
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
