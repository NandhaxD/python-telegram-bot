


from functools import wraps

from telegram.ext import CommandHandler, Filters




def command(command, filters=None, block=False):
    def decorator(func):
        handler = CommandHandler(command, func, filters=filters, block=block)
        application.add_handler(handler)
        return func
    return decorator


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
