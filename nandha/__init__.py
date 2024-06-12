


from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from pyrogram import Client, filters, types, enums, errors


import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)


TOKEN = "6913439784:AAEhIjZm-oSavOqtR1RXHQ3F__KqDDfCQRw"

app = ApplicationBuilder().token(TOKEN).build()

pgram = Client(
   name='TestNandha',
   api_id=9,
   api_hash="3975f648bb682ee889f35483bc618d1c",
   bot_token=TOKEN,
   plugins=dict(root='nandha')
)


