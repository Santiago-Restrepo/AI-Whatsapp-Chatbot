from dependencies.model import Model
from utils.generate_prompt_format import generate_prompt_format

model = Model("santi-restrepo-poli/Llama-2-7b-chat-hf")

def generate_llm_response(conversation_messages=None,**kwargs):
    context = generate_prompt_format(conversation_messages)
    user_message = kwargs['webhook_data']['message']
    
    print(f"Context: {context}")
    return model.predict(user_message, context=context)
    