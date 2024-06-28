

from telegram.ext import ContextTypes, CallbackContext
from telegram import Update, error, constants
from telegram.helpers import mention_html

from nandha.helpers.decorator import command, admin_check


@command(('adminlist','admins'))
@admin_check(None)
async def AdminList(update, context):
    message = update.message
    chat = message.chat
    bot = context.bot
    try:
      admins = await bot.get_administrators()
    except TelegramError as e:
        return await message.reply_text(
            text=f"❌ Error: {str(e)}"
        )

    text = f"<b>👮 Admins in {chat.title}</b>:"
    for user in admins:
         text += "➣ " + mention_html(user.id, user.first_name)
    return await message.reply_text(
         text=text, parse_mode=constants.ParseMode.HTML)
    




@command('del')
@admin_check('can_delete_messages')
async def delete(update: Update, context: CallbackContext):
    message = update.effective_message
    reply = message.reply_to_message
    if reply:
        try:
            await reply.delete()
            await message.delete()
        except error.TelegramError as e:
            return await message.reply_text("Error: {}".format(e))
    else:
        return await message.reply_text("What should I delete?")
