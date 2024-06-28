


from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import *


import logging
import aiohttp


LOGGER = logging.getLogger(__name__)

FORMAT = f"[Bot] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)



logging.getLogger('httpx').setLevel(logging.WARNING)


# Clients
app = ApplicationBuilder().token(TOKEN).build()

aiohttpsession = aiohttp.ClientSession()
