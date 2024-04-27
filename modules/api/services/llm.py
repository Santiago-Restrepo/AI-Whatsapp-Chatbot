from models.llm import Llm
from assistants import assistants

assistant = assistants['ollama-assistant']()

def generate_llm_response(conversation_messages=None,**kwargs):
    user_message = kwargs['webhook_data']['message']
    conversation_history = assistant.get_conversation_history(conversation_messages)
    
    return assistant.predict(user_message, conversation_history = conversation_history)

def get_llm_by_name(name, **kwargs):
    db = kwargs['db']
    return db.query(Llm).filter(Llm.name == name).first()
    
    