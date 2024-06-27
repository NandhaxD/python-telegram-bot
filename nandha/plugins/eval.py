

import io
import os
import textwrap
import traceback
import subprocess

from contextlib import redirect_stdout

from nandha import app, LOGGER, DEV_LIST
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext 
from nandha.helpers.decorator import command

namespaces = {}

def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            "__builtins__": globals()["__builtins__"],
            "bot": bot,
            "message": update.effective_message,
            "user": update.effective_user,
            "chat": update.effective_chat,
            "update": update,
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(f"IN: {update.effective_message.text} (user={user}, chat={chat})")


async def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            await bot.send_document(
                chat_id=update.effective_chat.id, 
                document=out_file
            )
    else:
        await bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"```python\n{output}```",
            parse_mode=ParseMode.MARKDOWN_V2,
        )


@command(('e','eval'))
async def evaluate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message.from_user.id not in DEV_LIST:
        return
    elif len(message.text.split()) < 2:
        return await message.reply_text(
          text="Write something to execute..."
        )

    bot = context.bot
    await send(await do(eval, bot, update), bot, update)

@command(('ex', 'py'))
async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message.from_user.id not in DEV_LIST:
        return
    elif len(message.text.split()) < 2:
        return await message.reply_text(
          text="Write something to execute..."
        )
      
    bot = context.bot
    await send(await do(exec, bot, update), bot, update)


def cleanup_code(code):
    if code.startswith("```") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:-1])
    return code.strip("` \n")


async def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(maxsplit=1)[1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open(
        "temp.txt", "w",
    ) as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return f"{e.__class__.__name__}: {e}"

    func = env["func"]

    try:
        with redirect_stdout(stdout):
            func_return = await func()
    except Exception as e:
        value = stdout.getvalue()
        return f"{value}{traceback.format_exc()}"
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f"{value}"
            else:
                try:
                    result = f"{repr(eval(body, env))}"
                except:
                    pass
        else:
            result = f"{value}{func_return}"
        if result:
            return result


@command(('sh','shell'))
async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.from_user.id not in DEV_LIST:
          return
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
  
    if not len(message.text.split()) >= 2:
       return await message.reply_text(
          "Write something to execute.."
       )
    code = message.text.split(maxsplit=1)[1]
    output = subprocess.getoutput(code)
    if len(str(output)) > 2000:
        path = f"{chat_id}_shell.txt"
        with open(path, "w") as file:
            file.write(output)
        return await message.reply_document(
            document=file,
            caption=f"<code>{code}</code>",
            parse_mode=ParseMode.MARKDOWN_V2
)                 
    else:
       return await message.reply_text(
text=
f"""
```Command:
{code}```
```py
{output}```
""",
parse_mode=ParseMode.MARKDOWN_V2
)         
       
 


@command('clearlocals')
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.from_user.id not in DEV_LIST:
        return

    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    await send("Cleared locals.", bot, update)

