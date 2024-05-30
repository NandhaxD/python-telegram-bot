


from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


import pyrogram
import logging
import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)


app = ApplicationBuilder().token(config.token).build()

pgram = pyrogram.Client(
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.token,
    plugins=dict(root='nandha')
)

