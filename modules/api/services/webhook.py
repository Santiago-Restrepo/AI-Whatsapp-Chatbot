from services import user as user_service, conversation as conversation_service, message as message_service


def initialize_conversation(**kwargs):
    user = user_service.create_user_if_not_exists(**kwargs)
    conversation, is_new_conversation = conversation_service.create_conversation_if_not_exists(
        user, **kwargs)
    conversation_service.unblock_conversation(conversation, **kwargs)
    return conversation, is_new_conversation


def run_conversation_flow(**kwargs):
    # Initialize conversation
    conversation, is_new_conversation = initialize_conversation(
        **kwargs)
    
    # Reply message
    if conversation.active:
        is_conversation_finished = conversation_service.end_conversation_if_needed(conversation,**kwargs)
        if is_new_conversation:
            message_service.send_initial_message(conversation, **kwargs)
        elif is_conversation_finished:
            message_service.send_final_message(conversation, **kwargs)
        else:
            message_service.send_message(conversation, **kwargs)
    else:
        message_service.send_wait_message(conversation, **kwargs)
