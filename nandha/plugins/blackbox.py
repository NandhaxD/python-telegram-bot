

import asyncio
import uuid
import re
import os
from aiohttp import FormData
from nandha import aiohttpsession as session, app
from nandha.helpers.decorator import command
from telegram import Update, constants
from telegram.ext import CallbackContext

def id_generator() -> str:
    return str(uuid.uuid4())

async def BlackBoxChat(user_id, messages):
  
      data = {
                "messages": messages,
                "user_id": user_id,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {},
            }
      headers = {"Content-Type": "application/json"}
      url = "https://www.blackbox.ai/api/chat"
  
      try:
          async with session.post(url, headers=headers, json=data) as response:
              response_text = await response.text()
              cleaned_response_text = re.sub(r'^\$?@?\$?v=undefined-rv\d+@?\$?|\$?@?\$?v=v\d+\.\d+-rv\d+@?\$?', '', response_text)
              text = cleaned_response_text.strip()[2:]
              if "$~~~$" in text:
                  text = re.sub(r'\$~~~\$.*?\$~~~\$', '', text, flags=re.DOTALL)
              return {'reply': text}
              
      except Exception as e:
          return {'reply': f'❌ Error: {str(e)}'}



@command(('blackbox', 'ask'))
async def blackbox(update: Update, context: CallbackContext) -> None:
    message = update.message
    bot = context.bot
    msg = await message.reply_text("⚡")

    if len(message.text.split()) == 1:
        return await msg.edit_text(
            text="*⚡ Enter some text ask.*", parse_mode=constants.ParseMode.MARKDOWN
        )
    else:
        prompt = message.text.split(maxsplit=1)[1]
        user_id = id_generator()
        image = None
        reply = message.reply_to_message
      
        if reply and (reply.photo or (reply.sticker and not reply.sticker.is_video)):
            file_name = f'blackbox_{message.chat.id}.jpeg'
            file = reply.sticker.file_id if reply.sticker else reply.photo[-1].file_id
            file_path = await (await bot.get_file(file)).download_to_drive(
                    custom_path=file_name
            )
          
            with open(file_path, 'rb') as file:
                os.remove(file_path)
                image = file.read()

        if image:
            data = FormData()
            data.add_field('fileName', file_name)
            data.add_field('userId', user_id)
            data.add_field('image', image, filename=file_name, content_type='image/jpeg')
            api_url = "https://www.blackbox.ai/api/upload"
            try:
                async with session.post(api_url, data=data) as response:
                    response_json = await response.json()
            except Exception as e:
                return await msg.edit_text(f"❌ Error: {str(e)}")

            messages = [{"role": "user", "content": response_json['response'] + "\n#\n" + prompt}]

            data = await BlackBoxChat(user_id, messages)
            return await msg.edit_text(text=data['reply'], parse_mode=constants.ParseMode.MARKDOWN)
          
        else:
            reply = message.reply_to_message
            if reply and reply.text:
                prompt = f"Old conversation:\n{reply.text}\n\nQuestion:\n{prompt}"
            messages = [{"role": "user", "content": prompt}]
            
            data = await BlackBoxChat(user_id, messages)
            return await msg.edit_text(text=data['reply'], parse_mode=constants.ParseMode.MARKDOWN)
          
