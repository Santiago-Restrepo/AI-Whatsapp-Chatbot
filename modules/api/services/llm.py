from dependencies.model import Model

model = Model("santi-restrepo-poli/Llama-2-7b-chat-hf")

def generate_llm_response(**kwargs):
    user_message = kwargs['webhook_data']['message']
    return model.predict(user_message)
