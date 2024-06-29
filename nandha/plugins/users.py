

from nandha import 
from telegram import constants
from nandha.helpers.decorator import command
from nandha.helpers.utils import get_media_id


@command('id')
async def TelegramID(update, context):
     '''
     Method command: /id 
     Method Info: reply to the message or just send to possible telegram ids.
     '''
     bot = context.bot
     message = update.effective_message
     reply = message.reply_to_message
  
     text = (
f"""
*You're Tg ID*: `{message.sender_chat.id if message.sender_chat else message.from_user.id}`
*Chat ID*: `{message.chat.id}`
*Msg ID*: `{message.message_id}`
"""
)  
     if reply:
          text += f"\n*Replied Tg ID*: `{reply.sender_chat.id if reply.sender_chat else reply.from_user.id}`"
          text += f"\n*Replied Msg ID*: `{reply.message.message_id}`"
          media_id = get_media_id(reply)
          if media_id:
               text += f"\n*Replied Media ID*: `{media_id}`"
     return await message.reply_text(
         text=text, parse_mode=constants.ParseMode.MARKDOWN
     )
          
       
     
     
