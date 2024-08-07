


from telegram import Update, constants, helpers, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from nandha import app, SUPPORT_CHAT
from nandha.helpers.decorator import command


@command('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    mention = helpers.mention_markdown(user_id=user.id, name=user.first_name, version=2)
  
    
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
    
    await message.reply_text(
        text=(f"*Hello there {mention}, I'm Simple bot made by @NandhaBots using [PythonTelegramBot](https://docs.python-telegram-bot.org) Library\.*"),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=buttons
    )

