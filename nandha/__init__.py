


from telegram.ext import ApplicationBuilder, PicklePersistence, ContextTypes, CommandHandler
from config import *


import logging
import aiohttp


LOGGER = logging.getLogger(__name__)

FORMAT = f"[Bot] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)



logging.getLogger('httpx').setLevel(logging.WARNING)


# Clients
persistence = PicklePersistence(filepath='nandha')
app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

aiohttpsession = aiohttp.ClientSession()
