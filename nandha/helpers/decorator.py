


from functools import wraps
from telegram import ChatMemberOwner, constants
from telegram.ext import CommandHandler, filters
from nandha import app, DEV_LIST, BOT_ID



def command(command, filters=None, block=False):
    def decorator(func):
        handler = CommandHandler(command, func, filters=filters, block=block)
        app.add_handler(handler)
        return func
    return decorator




def admin_check(permission):
    def decorator(func):
  #      @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            chat = update.effective_chat
            user = update.effective_user
            message = update.effective_message
            
            if hasattr(message, 'sender_chat'): 
                return
            
            STATUS = [
               constants.ChatMemberStatus.ADMINISTRATOR, 
               constants.ChatMemberStatus.OWNER
            ]
          
            user = await chat.get_member(user.id)
            bot = await chat.get_member(BOT_ID)
          
            if user.status in STATUS and bot.status in STATUS:
                if permission and not isinstance(user, ChatMemberOwner):
                    if not hasattr(user, permission) or not hasattr(bot, permission):
                        if not hasattr(user, permission):
                            await message.reply_text(
                                "You are missing {} permission.".format(permission)
                            )
                            return
                        else:
                            await message.reply_text(
                                "The bot is missing {} permission.".format(permission)
                            )
                            return
                return await func(update, context, *args, **kwargs)
            else:
                if user.status not in STATUS:
                    await message.reply_text(
                        "You are not an admin in this chat."
                    )
                    return
                else:
                    await message.reply_text(
                        "The bot is not an admin in this chat."
                    )
                    return
        return wrapper
    return decorator
  

    
def devs_only(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        message = update.effective_message
        if getattr(message, 'sender_chat'): return
        elif message.from_user.id not in DEV_LIST: return
        return await func(update, context, *args, **kwargs)
    return wrapper
  

# send_typing_action = send_action(ChatAction.TYPING)
# send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
# send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator
