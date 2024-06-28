



from telegram.constants import MessageEntityType


def extract_user(message):
    text = message.text
    user_id = None
    reply = message.reply_to_message
  
    if len(text.split()) >= 2:
        text_mention_user_ids = [entity.user.id for entity in message.entities if entity.type == MessageEntityType.TEXT_MENTION]
      
        if text_mention_user_ids:
            user_id = text_mention_user_ids[0]
          
        elif text.split()[1].isdigit():
            user_id = int(text.split()[1])
          
    elif reply and reply.from_user:
          user_id = reply.from_user.id
    else:
          user_id = message.from_user.id
      
    return user_id
    
