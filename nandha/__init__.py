


from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler



import logging



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)


TOKEN = "6913439784:AAEhIjZm-oSavOqtR1RXHQ3F__KqDDfCQRw"

app = ApplicationBuilder().token(TOKEN).build()



