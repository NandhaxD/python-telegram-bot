


from telegram import Update, constants, helpers, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from nandha import app, SUPPORT_CHAT
from nandha.sql.users import add_user, get_all_users

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot = context.bot 
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    mention = helpers.mention_markdown(user_id=user_id, name=user_name, version=2)
  
    if not user_id in get_all_users():
        add_user(user_id)
        await bot.send_message(
            chat_id=SUPPORT_CHAT,
            text=(
f"""              
⚡ *New User*:

*🆔 ID*: `{user_id}`
*🙋 User*: *{mention}*

"""),
          parse_mode=constants.ParseMode.MARKDOWN_V2)

  
    
    keyboard = [
        [
            InlineKeyboardButton("Group 🌟", url="NandhaChat.t.me"),
            InlineKeyboardButton("Channel 🌟", url="NandhaBots.t.me"),
        ],
        [
            InlineKeyboardButton("💀 Nandha 💀", url=f"tg://user?id={user_id}")
        ]
    ]

    buttons = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(
        chat_id=update.effective_chat.id,
        text=(f"*Hello there {mention}, I'm Simple bot made by @NandhaBots using [PythonTelegramBot](https://docs.python-telegram-bot.org) Library\.*"),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=buttons)

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)
