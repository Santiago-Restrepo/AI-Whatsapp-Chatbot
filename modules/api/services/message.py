from clients.twilio import client
from services import llm as llm_service
from schemas.message import MessageCreate
from models.conversation import Conversation
from models.message import Message
from datetime import datetime

MESSAGES = {
    'initial': 'Bienvenido al chatbot de la Personería Distrital De Medellín, nuestra conversación finalizará una vez envíes la palabra *finalizar* o pasadas 72 horas de haberse iniciado. ¿En qué puedo ayudarte el día de hoy?',
    'final': 'Hasta pronto!'
}


def send_message(conversation: Conversation, default_body_response: str = None, **kwargs):
    wa_id = kwargs['webhook_data']['wa_id']
    message = kwargs['webhook_data']['message']
    if default_body_response:
        response = default_body_response
    else:
        response = llm_service.generate_llm_response(conversation_messages=conversation.messages, **kwargs)
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=response,
        to='whatsapp:+{}'.format(wa_id)
    )
    return create_message(message, response, conversation.id, **kwargs)


def create_message(body: str, response: str, conversation_id: int, **kwargs):
    db = kwargs['db']
    message = MessageCreate(body=body, response=response,
                            conversation_id=conversation_id, created_at=datetime.now())
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def send_initial_message(conversation: Conversation, **kwargs):
    send_message(conversation, MESSAGES['initial'], **kwargs)


def send_final_message(conversation: Conversation, **kwargs):
    send_message(conversation, MESSAGES['final'], **kwargs)
