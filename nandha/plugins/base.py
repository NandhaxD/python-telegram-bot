


from telegram import Update, constants, helpers, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from nandha import app, SUPPORT_CHAT
from nandha.sql.users import add_user, get_all_users
from nandha.sql.chats import get_all_chats, add_chat

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user
    mention = helpers.mention_markdown(user_id=user.id, name=user.first_name, version=2)
  
    if chat.type == constants.ChatType.PRIVATE:
        if not user.id in get_all_users():
             add_user(user.id)
             await bot.send_message(
            chat_id=SUPPORT_CHAT,
            text=(
f"""              
⚡ *New User*:

*🆔 ID*: `{user.id}`
*🙋 User*: *{mention}*

"""),
          parse_mode=constants.ParseMode.MARKDOWN_V2)

    else:
        if not chat.id in get_all_chats():
            add_chat(chat.id)
            await bot.send_message(
            chat_id=SUPPORT_CHAT,
            text=(
f"""              
⚡ *New Chat*:

*🆔 ID*: `{chat.id}`
*🙋 Chat*: *{chat.title}*

"""),
          parse_mode=constants.ParseMode.MARKDOWN_V2)

    
    keyboard = [
        [
            InlineKeyboardButton("Group 🌟", url="NandhaChat.t.me"),
            InlineKeyboardButton("Channel 🌟", url="NandhaBots.t.me"),
        ],
        [
            InlineKeyboardButton("💀 Nandha 💀", url=f"tg://user?id={user.id}")
        ]
    ]

    buttons = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(
        chat_id=chat.id,
        text=(f"*Hello there {mention}, I'm Simple bot made by @NandhaBots using [PythonTelegramBot](https://docs.python-telegram-bot.org) Library\.*"),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=buttons
    )

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)
