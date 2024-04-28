from models.user import User
from models.conversation import Conversation
from schemas.conversation import ConversationCreate
from services.llm import get_llm_by_name
from datetime import datetime
from sqlalchemy import desc


def create_conversation_if_not_exists(user: User, **kwargs):
    conversation = get_conversation_by_user_id(user.id, **kwargs)
    if not conversation:
        conversation = create_conversation(user, **kwargs)
        is_new_conversation = True
        return conversation, is_new_conversation
    is_new_conversation = len(conversation.messages) == 0
    return conversation, is_new_conversation


def get_conversation_by_user_id(user_id: int, **kwargs):
    db = kwargs['db']
    return db.query(Conversation).filter(Conversation.user_id == user_id, Conversation.finished_at == None).first()


def create_conversation(user: User, **kwargs):
    db = kwargs['db']
    llm = get_llm_by_name('santi-restrepo-poli/Llama-2-7b-chat-hf', **kwargs)
    if not llm:
        raise Exception('Llm not found')
    conversation_status = define_conversation_status(**kwargs)
    conversation_started_at = datetime.now() if conversation_status else None
    print('conversation_started_at', conversation_started_at)
    conversation = ConversationCreate(user_id=user.id, llm_id=llm.id, active=conversation_status, started_at=conversation_started_at)
    db_conversation = Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def define_conversation_status(**kwargs):
    db = kwargs['db']
    # Check if there is another active conversation
    active_conversations = db.query(Conversation).filter(Conversation.active == True, Conversation.finished_at == None).all()
    if active_conversations:
        return False
    return True

def end_conversation_if_needed(conversation: Conversation, **kwargs):
    message = kwargs['webhook_data']['message']
    if message.lower() == 'finalizar' or conversation_timeout(conversation, **kwargs):
        return end_conversation(conversation, **kwargs)
    return False

def conversation_timeout(conversation: Conversation, **kwargs):
    conversation_elapsed_time = (datetime.now() - conversation.started_at).total_seconds()
    return conversation_elapsed_time > kwargs['timeout']

def end_conversation(conversation: Conversation, **kwargs):
    db = kwargs['db']
    conversation.finished_at = datetime.now()
    conversation.active = False
    db.commit()
    db.refresh(conversation)
    return True

def set_next_conversation_as_active(conversation, db):
    conversation = db.query(Conversation).filter(Conversation.active == False, Conversation.id != conversation.id).order_by(desc(Conversation.created_at)).first()
    if not conversation:
        return
    conversation.active = True
    conversation.started_at = datetime.now()
    return conversation

def unblock_conversation(conversation: Conversation, **kwargs):
    db = kwargs['db']
    active_conversation = db.query(Conversation).filter(Conversation.active == True, Conversation.id != conversation.id).first()
    if not active_conversation:
        return
    end_conversation_if_needed(active_conversation, **kwargs)
