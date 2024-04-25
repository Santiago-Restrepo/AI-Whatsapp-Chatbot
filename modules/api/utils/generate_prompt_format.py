
def generate_prompt_format(messages):
  formatted_messages = []
  for msg in messages:
      formatted_msg = f'<s>[INST] {msg.body} [/INST] {msg.response}</s>'
      formatted_messages.append(formatted_msg)

  formatted_messages = '\n'.join(formatted_messages)
  return formatted_messages