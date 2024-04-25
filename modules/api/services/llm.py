from dependencies.model import Model
from utils.generate_prompt_format import generate_prompt_format
from models.llm import Llm

model = Model("santi-restrepo-poli/Llama-2-7b-chat-hf", True)

def generate_llm_response(conversation_messages=None,**kwargs):
    context = generate_prompt_format(conversation_messages)
    user_message = kwargs['webhook_data']['message']
    
    return model.predict(user_message, context=context)

def get_llm_by_name(name, **kwargs):
    db = kwargs['db']
    return db.query(Llm).filter(Llm.name == name).first()
    
    