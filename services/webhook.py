from sqlalchemy.orm import Session
from clients.twilio import client
from services.user import create_user_if_not_exists
def receive_whatsapp_message(db: Session, body: str, wa_id: str):
    create_user_if_not_exists(db, wa_id)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='You said: {}'.format(body),
        to='whatsapp:+{}'.format(wa_id)
    )

    return {"message_id": message.sid}  # Return only the message ID

