from clients.twilio import client
from services import llm as llm_service
from schemas.message import MessageCreate
from models.conversation import Conversation
from models.message import Message
from datetime import datetime

MESSAGES = {
    'initial': 'Bienvenido al chatbot de la Personería Distrital De Medellín, la conversación finalizará una vez envíe la palabra finalizar o pasada 1 hora de haberse iniciado. ¿En qué podemos ayudarle el día de hoy?',
    'final': 'Hasta pronto!',
    'wait': 'Tu consulta está siendo procesada, por favor espere un momento...',
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

def send_wait_message(conversation: Conversation, **kwargs):
    send_message(conversation, MESSAGES['wait'], **kwargs)
