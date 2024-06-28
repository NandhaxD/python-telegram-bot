

from telegram.ext import ContextTypes, CallbackContext
from telegram import Update, error, constants
from telegram.helpers import mention_html

from nandha.helpers.decorator import command, admin_check


@command(('adminlist','admins'))
@admin_check(None)
async def AdminList(update, context):
    message = update.message
    chat = message.chat

    msg = await message.reply_text("⚡ Fetching admins please wait...")
    try:
      admins = await chat.get_administrators()
    except error.TelegramError as e:
        return await msg.edit_text(
            text=f"❌ Error: {str(e)}"
        )

    text = f"<b>👮 Admins in {chat.title}</b>:"
    for user in admins:
         text += "➣ " + mention_html(user.id, user.first_name)
    return await msg.edit_text(
         text=text, parse_mode=constants.ParseMode.HTML)
    




@command('del')
@admin_check('can_delete_messages')
async def delete(update, context):
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
