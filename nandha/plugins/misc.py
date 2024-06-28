import asyncio
import uuid
import os

from aiohttp import FormData
from nandha import aiohttpsession as session, app
from nandha.helpers.decorator import command

@command(('tm','tgm'))
async def Telegraph(update, context):
    message = update.message
    bot = context.bot

    api_url = "https://telegra.ph/upload"

    reply = message.reply_to_message
    if not reply:
        return await message.reply_text(
            text="⚡ Reply to the animation (GIF) or a photo to upload in graph.org"
        )
    
    if reply.photo:
        file_name = f"{str(uuid.uuid4())}.jpeg"
        media_type = "image/jpeg"
        file_id = reply.photo[3].file_id
    elif reply.animation:
        file_name = reply.animation.file_name
        media_type = reply.animation.mime_type
        file_id = reply.animation.file_id
    else:
        return await message.reply_text(
            text="⚡ Reply to the animation (GIF) or a photo to upload in grap.org"
        )
    
    msg = await message.reply_text("Downloading...")
    file = await bot.get_file(file_id)
    file_path = await file.download_to_drive(
        custom_path=file_name
    )
    
    with open(file_path, 'rb') as f:
         file_contents = f.read()
    
    form_data = FormData()
    form_data.add_field("file", file_contents, filename=file_name, content_type=media_type)
    async with session.post(api_url, data=form_data) as response:
         os.remove(file_path)
         if response.status == 200:
              data = await response.json()
              if isinstance(data, dict):
                    return await msg.edit_text("❌ problem while uploading file.")
              src = data[0].get('src')
              url = 'https://graph.org' + src
              return await msg.edit_text(url)
         else:
             return await msg.edit_text(
                        text=f"❌ can't upload status code: {str(response.status)}"
                    )
