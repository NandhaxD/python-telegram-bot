

from telegram.ext import ContextTypes, CallbackContext
from telegram import Update

from nandha.helpers.decorator import command, admin_check


@command('del')
@admin_check(permission='can_delete_messages')
async def delete(update: Update, context: CallbackContext):
    message = update.effective_message
    reply = message.reply_to_message
    if reply:
        try:
            await reply.delete()
            await message.delete()
        except TelegramError as e:
            return await message.reply_text("Error: {}".format(e))
    else:
        return await message.reply_text("What should I delete?")
