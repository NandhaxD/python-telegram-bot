



from telegram.constants import MessageEntityType

def extract_user(message):
    text = message.text
    user_id = None
    if message.entities and len(text.split()) >= 2:
        text_mentions = [ entity.user for entity in message.entities if entity.type in (MessageEntityType.TEXT_MENTION, MessageEntityType.MENTION) ]
        if text_mentions:
            user_id = text_mentions[0].id
    else:
        reply = message.reply_to_message
        if reply and not reply in (reply.sender_chat, reply.from_user.is_bot):
            user_id = reply.from_user.id
    return user_id
        
    

