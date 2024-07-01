


from functools import wraps
from telegram import ChatMemberOwner, ChatMemberAdministrator, constants
from telegram.ext import CommandHandler, filters
from nandha import app, DEV_LIST, BOT_ID



def command(command, filters=None, block=False):
    def decorator(func):
        prefix = ['!', '?', '$', '/', '\\']
        handler = CommandHandler(prefix, command, func, filters=filters, block=block)
        app.add_handler(handler)
        return func
    return decorator





def admin_check(permission: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            chat = update.effective_chat
            user = update.effective_user
            message = update.effective_message

            IS_PRIVATE = message.chat.type == constants.ChatType.PRIVATE
          
            if getattr(message, 'sender_chat', None) or IS_PRIVATE: 
                  return
            
            STATUS = [
                constants.ChatMemberStatus.ADMINISTRATOR, 
                constants.ChatMemberStatus.OWNER
            ]
            
            user_member = await chat.get_member(user.id)
            bot_member = await chat.get_member(context.bot.id)
            
            if user_member.status in STATUS and bot_member.status in STATUS:
                if isinstance(user_member, ChatMemberOwner):
                    return await func(update, context, *args, **kwargs)
                elif isinstance(user_member, ChatMemberAdministrator):
                    if permission:
                        user_permission = getattr(user_member, permission, False)
                        bot_permission = getattr(bot_member, permission, False)
                        if not user_permission:
                            await message.reply_text(
                                f"*You are missing the [ {permission} ] permission.*",
                                parse_mode=constants.ParseMode.MARKDOWN
                            )
                            return
                        elif not bot_permission:
                            await message.reply_text(
                                f"The bot is missing the [ {permission} ] permission.",
                                parse_mode=constants.ParseMode.MARKDOWN
                            )
                            return
                    return await func(update, context, *args, **kwargs)
            else:
                if user_member.status not in STATUS:
                    await message.reply_text(
                        "*You are not an admin in this chat.*",
                      parse_mode=constants.ParseMode.MARKDOWN
                    )
                else:
                    await message.reply_text(
                        "*The bot is not an admin in this chat.*",
                        parse_mode=constants.ParseMode.MARKDOWN
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
