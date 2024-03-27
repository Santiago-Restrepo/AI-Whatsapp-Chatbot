from sqlalchemy.orm import Session
from clients.twilio import client

def receive_whatsapp_message(db: Session, body: str, wa_id: str):
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='You said: {}'.format(body),
        to='whatsapp:+{}'.format(wa_id)
    )

    return {"message_id": message.sid}  # Return only the message ID

