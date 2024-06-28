import asyncio
import uuid

from aiohttp import MultipartWriter

from nandha import aiohttpsession as session, app
from nandha.helpers.decorator import command

@command(('tm','tgm'))
async def Telegraph(update, context):
     message = update.message
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
     

     mpwriter = MultipartWriter()
     part = mpwriter.append(Body(file_path, filename=file_name, contentType=media_type))
     part.set_content_disposition('form-data', filename=file_name)
     
     async with session.post(api_url, data=mpwriter) as response:
        if response.status == 200:
            data = await response.json()
            if isinstance(data, dict):
                return await msg.edit_text("❌ Image was upload but error while getting file link.")
            src = data[0].get('src')
            url = 'https://graph.org' + src
            return await msg.edit_text(url)
        else:
           return await msg.edit_text(
               text=f"❌ can't upload status code: {str(response.status)}"
           )
