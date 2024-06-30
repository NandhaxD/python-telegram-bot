


from bs4 import BeautifulSoup
from urllib.parse import quote
from nandha import aiohttpsession as session, app
from nandha.helpers.decorator import command
from telegram import constants, InputMediaPhoto


import random

async def fetch_wallpapers(query: str = None, tag: str = 'anime'):
    '''
    parameter: query - optional, tag - default anime
    return: list images data with tile and url values
    Scaping website: wallpapers.com
    
    Made by @NandhaBots & thank for love & support
    '''
    images_data = []
    if not query:
        url = f"https://wallpapers.com/search/{tag}"
        async with session.get(url) as response:
              soup = BeautifulSoup(await response.text(), 'html.parser')
              page_counter = soup.find('div', class_='page-counter mobi')
              total_pages = int(page_counter.text.split()[-1])
              page = random.randint(1, total_pages)
              url = f"https://wallpapers.com/search/{tag}?p={page}"
              async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    for item in soup.find_all('li', class_='content-card'):
                        a_tag = item.find('a')
                        img_tag = item.find('img')
                        title = a_tag.get('title') if a_tag else None
                        img_url = img_tag.get('data-src') if img_tag else None
                        if title and img_url:
                            image_url = 'https://wallpapers.com' + img_url
                            images_data.append({'title': title, 'url': image_url})

    else:
        url = f"https://wallpapers.com/search/{quote(query)}"
        async with session.get(url) as response:
             soup = BeautifulSoup(await response.text(), 'html.parser')
             page_counter = soup.find('div', class_='page-counter mobi')
             if not page_counter:
                  return images_data
             total_pages = int(page_counter.text.split()[-1])
             page = random.randint(1, total_pages)
             url = f"https://wallpapers.com/search/{quote(query)}?p={page}"
             async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    for item in soup.find_all('li', class_='content-card'):
                        a_tag = item.find('a')
                        img_tag = item.find('img')
                        title = a_tag.get('title') if a_tag else None
                        img_url = img_tag.get('data-src') if img_tag else None
                        if title and img_url:
                            image_url = 'https://wallpapers.com' + img_url
                            images_data.append({'title': title, 'url': image_url})

    return images_data


@command(('wall', 'wallpaper', 'wallpapers'))
async def Wallpapers_com(update, context):
      message = update.message
      if len(message.text.split()) == 1:
          data = await fetch_wallpapers()
      else:
          data = await fetch_wallpapers(
              query = message.text.split(maxsplit=1)[1]
          )
        
      media = []
      text = ""
    
      if len(data) == 0:
          return await message.reply_text(
             "⚡ No media fetched"
          )
      msg = await message.reply_text(
              f"⚡ Successfully fetched {len(data)} sending media..."
      )

      limits = data[:8]
      
      for idx, image_key in enumerate(limits, start=1):
                
                if idx == len(limits):
                    text += f"\n[`{idx}`], *{image_key['title']}*"
                    media.append(
                       InputMediaPhoto(
                         media=image_key['url'],
                         caption=text
                       )
                )
                else:
                    text += f"\n[`{idx}`], *{image_key['title']}*"
                    media.append(
                       InputMediaPhoto(
                         media=image_key['url']
                       )
                   )
      try:
          return await message.reply_media_group(
                     media=media, quote=True, parse_mode=constants.ParseMode.MARKDOWN
              )
      except Exception as e:
                return await msg.edit_text(f"❌ Error: {str(e)}")
          

  


