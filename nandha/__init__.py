


from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import *


import logging





logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)



app = ApplicationBuilder().token(TOKEN).build()
