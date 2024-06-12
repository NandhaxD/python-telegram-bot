

from pyrogram import filters, types, enums, errors
from nandha import pgram


import os
import io
import sys
import time
import config
import traceback
import subprocess



DEVS = [
  5015417782,
  7019511932,
  6381687972,
  5696053228
]

async def aexec(code, pgram, m, message, r, ruser, my, p):
    exec(
        "async def __aexec(pgram, m, message, r, ruser, my, p): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](pgram, m, message, r, ruser, my, p)
  




@pgram.on_message(filters.user(DEVS) & filters.command('sh', prefixes=['!','.','?']))
async def shell(_, message):
   if len(message.text.split()) > 1:
        code = message.text.split(None, 1)[1]
        shell = subprocess.getoutput(code)
        if len(shell) > 4096:
           filename = "shell.txt"
           with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(shell))
           await message.reply_document(
               document=filename,
               caption=str(code),
               quote=True,
                )
            os.remove(filename)
            return
        else:
            return await message.reply_text(
               text=f"<pre language='python'>\nSHELL output:\n{shell}</pre>", 
               quote=True,
               parse_mode=enums.ParseMode.HTML)
    

@pgram.on_message(filters.user(DEVS) & filters.command("ev", prefixes=['!','.','?']))
async def evaluate(pgram , message):
    status_message = await message.reply_text("`Running ...`")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    start_time = time.time()

    r = message.reply_to_message	
    m = message
    p = print
    my = getattr(m, m.from_user, None)
    ruser = getattr(m, r.from_user, None)

    if r:
        reply_to_id = r.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, pgram, m, message, r, ruser, my, p)
    except Exception:
        exc = traceback.format_exc()
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
    taken_time = round((time.time() - start_time), 3)
    output = evaluation.strip()
	
    final_output = "<pre>Command:</pre><pre language='python'>{}</pre> \n<pre>Takem Time To Output: {}'s:</pre><pre language='python'>{}</pre>".format(cmd, taken_time, output)
	
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            quote=True,
            
        )
        os.remove(filename)
        await status_message.delete()
        return
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.HTML)
        return 
