

from telegram.ext import ContextTypes, CallbackContext
from telegram import Update, error, constants, ChatMemberOwner
from telegram.helpers import mention_html
from nandha.helpers.utils import extract_user
from nandha.helpers.decorator import command, admin_check


@command('invite')
@admin_check()
async def GetInvite(update, context):
    message = update.message
    bot = context.bot
    chat = await bot.get_chat(message.chat.id)
    link = chat.invite_link
    await message.reply_text(
        text=f"<b>✨ {chat.title} Invite Link</b>: {link}"
    )
    
  


@command('unban')
@admin_check('can_restrict_members')
async def UnBanChatMember(update, context):
    message = update.message
    reply = message.reply_to_message
    chat = message.chat
    user = message.from_user
    bot = context.bot
    
    if getattr(reply, 'sender_chat', None):
        sender_chat = reply.sender_chat
        try:
           success = await bot.unban_chat_sender_chat(
               chat_id=chat.id,
               sender_chat_id=sender_chat.id
        )
           if success:
                return await message.reply_text(
text=(
f"""
<b>⚡ Channel {sender_chat.title} UnBanned in {chat.title}.</b>
"""), parse_mode=constants.ParseMode.HTML
            )
        except TelegramError as e:
            return await message.reply_text(
              text=f"❌ Error: {str(e)}"
        )

            
               
    user_id = extract_user(message)
  
    if not user_id or user_id == user.id:
        return await message.reply_text(
           "Reply to a user or provide their id / mention to UnBan !"
        )
      
    try:
      
        member = await bot.get_chat_member(chat.id, user_id)
      
        success = await bot.unban_chat_member(
             chat_id=chat.id,
             user_id=member.user.id
        )
        if success:
            member_mention = mention_html(member.user.id, member.user.first_name)
            return await message.reply_text(
text=(
f"""
<b>⚡ {'Bot' if member.user.is_bot else 'User'} {member_mention} UnBanned in {chat.title}.</b>
"""), parse_mode=constants.ParseMode.HTML
            )
    except error.TelegramError as e:
        return await message.reply_text(
          text=f"❌ Error: {str(e)}"
        )




@command('ban')
@admin_check('can_restrict_members')
async def BanChatMember(update, context):
    message = update.message
    reply = message.reply_to_message
    chat = message.chat
    user = message.from_user
    bot = context.bot
    
    if getattr(reply, 'sender_chat', None):
        sender_chat = reply.sender_chat
        try:
           success = await bot.ban_chat_sender_chat(
               chat_id=chat.id,
               sender_chat_id=sender_chat.id
        )
           if success:
                return await message.reply_text(
text=(
f"""
<b>⚡ Channel {sender_chat.title} Banned in {chat.title}.</b>
"""), parse_mode=constants.ParseMode.HTML
            )
        except TelegramError as e:
            return await message.reply_text(
              text=f"❌ Error: {str(e)}"
        )

            
               
    user_id = extract_user(message)
  
    if not user_id or user_id == user.id:
        return await message.reply_text(
           "Reply to a user or provide their id / mention to Ban !"
        )
      
    try:
      
        member = await bot.get_chat_member(chat.id, user_id)
      
        success = await bot.ban_chat_member(
             chat_id=chat.id,
             user_id=member.user.id
        )
        if success:
            member_mention = mention_html(member.user.id, member.user.first_name)
            return await message.reply_text(
text=(
f"""
<b>⚡ {'Bot' if member.user.is_bot else 'User'} {member_mention} Banned in {chat.title}.</b>
"""), parse_mode=constants.ParseMode.HTML
            )
    except error.TelegramError as e:
        return await message.reply_text(
          text=f"❌ Error: {str(e)}"
        )


@command(('adminlist','admins'))
@admin_check()
async def AdminList(update, context):
    message = update.message
    chat = message.chat

    msg = await message.reply_text("⚡ Fetching Admins...")
    try:
        admins = await chat.get_administrators()
    except error.TelegramError as e:
        return await msg.edit_text(
            text=f"❌ Error: {str(e)}"
        )      

    owner = next((mem for mem in admins if isinstance(mem, ChatMemberOwner)), None)
    if owner:
        text = f"🧑‍✈️ <b>Stuff's in {chat.title}</b>:\n\n👑 <b>Owner</b>: {mention_html(owner.user.id, owner.user.first_name)}\n\n👮 <b>Admins</b>:\n\n"
    else:
        text = f"👮 <b>Admins in {chat.title}</b>:\n\n"


    for mem in admins:
        if isinstance(mem, ChatMemberOwner):
             continue
        text += f"➣ <b>{mention_html(mem.user.id, mem.user.first_name)}</b>\n"

    return await msg.edit_text(
        text=text, parse_mode=constants.ParseMode.HTML
    )
  


@command('del')
@admin_check('can_delete_messages')
async def delete(update, context):
    message = update.effective_message
    reply = message.reply_to_message
    if reply:
        try:
            await reply.delete()
            await message.delete()
        except error.TelegramError as e:
            return await message.reply_text("Error: {}".format(e))
    else:
        return await message.reply_text("What should I delete?")
