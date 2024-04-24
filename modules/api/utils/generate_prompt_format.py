from models.message import Message

def generate_prompt_format(messages: list[Message]):
  formatted_messages = []
  for msg in messages:
      formatted_msg = f'<s>[INST] {msg["message"]} {msg["response"]}[/INST]</s>'
      formatted_messages.append(formatted_msg)
  return formatted_messages