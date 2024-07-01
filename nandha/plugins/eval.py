

import io
import os
import sys
import traceback
import subprocess

from contextlib import redirect_stdout

from nandha import app, DEV_LIST
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext 
from nandha.helpers.decorator import command, devs_only



async def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            await bot.send_document(
                chat_id=update.effective_chat.id, 
                document=out_file
            )
            os.remove(out_file)
    else:
        await bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"```python\n{msg}```",
            parse_mode=ParseMode.MARKDOWN_V2,
        )



async def aexec(code, bot, message, m, r, my, chat, ruser):
    exec(
        "async def __aexec(bot, message, m, r, my, chat, ruser): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](bot, message, m, r, my, chat, ruser)


 
def p(*args, **kwargs):
    print(*args, **kwargs)
	   

@command(('e','eval'))
@devs_only
async def evaluate(update, context):
    message = update.effective_message
    if len(message.text.split()) < 2:
        return await message.reply_text(
          text="Write something to execute..."
        )

    bot = context.bot
    stdout = io.StringIO()
  
    r = message.reply_to_message
    m = message
    ruser = getattr(r, 'from_user', None)
    my = getattr(message, 'from_user', None)
    chat = getattr(message, 'chat', None)

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
  
    try:
       await aexec(
		code=cmd, 
		bot=bot, 
		m=message, 
		r=r,
		chat=chat,
		message=message,
		ruser=ruser,
		my=my
       )
    except Exception as e:
        exc = traceback.format_exception_only(type(e), e)[-1].strip()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
  
    sys.stdout = old_stdout
    sys.stderr = old_stderr
  
    evaluation = ""
  
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
      
    output = evaluation.strip()
    await send(output, bot, update)

  
    
  
@command(('sh','shell'))
@devs_only
async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
  
    if not len(message.text.split()) >= 2:
       return await message.reply_text(
          "Write something to execute.."
       )
    code = message.text.split(maxsplit=1)[1]
    output = subprocess.getoutput(code)
    await send(output, bot, update)

