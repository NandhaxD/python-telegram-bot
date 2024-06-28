

from telegram.ext import CallbackContext
from telegram import Update

from nandha.helpers.decorator import command, admin_check


@command('del')
@admin_check('can_delete_messages')
async def delete(update: Update, context: CallbackContext):
      message = update.effective_message
      reply = message.reply_to_message:
      if reply:
         await reply.delete()
         await message.delete()
      else:
          return await message.reply_text(
              text="What should i delete ?"
          )
