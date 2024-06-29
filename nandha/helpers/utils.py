



from telegram.constants import MessageEntityType


def get_media_id(message):
    '''
    Info: 
      returns a tuple of (type, file_id) of any media in
      message if no media will return (None, None)
    '''
    
    media_types = {
        'photo': message.photo,
        'animation': message.animation,
        'document': message.document,
        'sticker': message.sticker,
        'voice': message.voice,
        'audio': message.audio
    }
    
    for media_type, media in media_types.items():
        if media:
            if media_type == 'photo':
                return media_type, media[-1].file_id
            else:
                return media_type, media.file_id
    
    return None, None
  



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
    
