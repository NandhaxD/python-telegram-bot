



from telegram.constants import MessageEntityType


def extract_user(message):
    text = message.text
    user_id = None

    if message.entities and len(text.split()) >= 2:
        text_mention_user_ids = [entity.user.id for entity in message.entities if entity.type == MessageEntityType.TEXT_MENTION]
        if text_mention_user_ids:
            user_id = text_mention_user_ids[0]
        else:
            mention_usernames = [text.split()[1] for entity in message.entities if entity.type == MessageEntityType.MENTION]
            if mention_usernames:
                user_id = mention_usernames[0]
    else:
        reply = message.reply_to_message
        if reply and reply.from_user and not reply.from_user.is_bot:
            user_id = reply.from_user.id

    return user_id
    
