from models.user import User
from models.conversation import Conversation
from schemas.conversation import ConversationCreate
from datetime import datetime


def create_conversation_if_not_exists(user: User, **kwargs):
    conversation = get_conversation_by_user_id(user.id, **kwargs)
    is_new_conversation = False
    if not conversation:
        conversation = create_conversation(user, **kwargs)
        is_new_conversation = True
        return conversation, is_new_conversation
    return conversation, is_new_conversation


def get_conversation_by_user_id(user_id: int, **kwargs):
    db = kwargs['db']
    return db.query(Conversation).filter(Conversation.user_id == user_id, Conversation.finished_at == None).first()


def create_conversation(user: User, **kwargs):
    db = kwargs['db']
    conversation = ConversationCreate(user_id=user.id, llm_id=1)
    db_conversation = Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def end_conversation_if_needed(conversation: Conversation, **kwargs):
    message = kwargs['webhook_data']['message']
    if message.lower() == 'finalizar':
        return end_conversation(conversation, **kwargs)
    return False


def end_conversation(conversation: Conversation, **kwargs):
    db = kwargs['db']
    conversation.finished_at = datetime.now()
    db.commit()
    db.refresh(conversation)
    return True
