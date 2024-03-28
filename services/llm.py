from clients.anthropic import client


def generate_llm_response(**kwargs):
    user_message = kwargs['webhook_data']['message']
    # message = client.messages.create(
    #     model="claude-3-opus-20240229",
    #     max_tokens=100,
    #     temperature=0,
    #     system="Today is March 27, 2024.",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": user_message
    #                 }
    #             ]
    #         }
    #     ]
    # )
    message = "Response: {}".format(user_message)
    return message
