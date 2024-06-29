

from telegram import constants
from nandha.helpers.decorator import command
from nandha.helpers.utils import get_media_id



@command('info')
async def UserInfo(update, context):
     '''
      Method: /info username | id
      Method info: get user info
     '''
     pass


@command('id')
async def GetTelegramID(update, context):
     '''
     Method command: /id 
     Method Info: reply to the message or just send to get the possible telegram ids.
     '''
     bot = context.bot
     message = update.effective_message
     reply = message.reply_to_message

     if len(message.text.split()) == 2 and message.text.split()[1].isdigit():
             try:
                user = await bot.get_chat(message.text.split()[1])
                text = f"*User {user.first_name}'s ID*: `{user.id}`"
                return await message.reply_text(
                      text, parse_mode=constants.ParseMode.MARKDOWN
                )
             except Exception as e:
                    return await message.reply_text(
                          text=f"❌ Error: {str(e)}"
                    )
             
          
     text = (
f"""
*🚹 You're Tg ID*: `{message.sender_chat.id if message.sender_chat else message.from_user.id}`
*🗨️ Chat ID*: `{message.chat.id}`
*📝 Msg ID*: `{message.message_id}`
"""
)  
     if reply:
          text += f"\n*🚹 Replied Tg ID*: `{reply.sender_chat.id if reply.sender_chat else reply.from_user.id}`"
          text += f"\n*📝 Replied Msg ID*: `{reply.message_id}`"
          media_type, media_id = get_media_id(reply)
          if media_type and media_id:
               text += f"\n*📁 Replied {media_type.capitalize()} ID*: `{media_id}`"
     return await message.reply_text(
         text=text, parse_mode=constants.ParseMode.MARKDOWN
     )
          
       
     
     
