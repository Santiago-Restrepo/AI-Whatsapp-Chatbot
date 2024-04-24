from schemas.message import Message

def generate_prompt_format(messages: list[Message]):
  formatted_messages = []
  for msg in messages:
      formatted_msg = f'<s>[INST] {msg["body"]} {msg["response"]}[/INST]</s>'
      formatted_messages.append(formatted_msg)

  formatted_messages = '\n'.join(formatted_messages)
  return formatted_messages