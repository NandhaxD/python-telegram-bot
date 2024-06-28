

from telegram.ext import ContextTypes, CallbackContext
from telegram import Update, error, constants, ChatMemberOwner
from telegram.helpers import mention_html
from nandha.helpers.utils import extract_user
from nandha.helpers.decorator import command, admin_check



@command('ban')
@admin_check('can_restrict_members')
async def BanChatMember(update, context):
    message = update.message
    chat = message.chat
    user = message.from_user
    bot = context.bot
  
    user_id = extract_user(message)
    if not user_id or user_id == user.id:
        return await message.reply_text(
           "Reply to a user or give their id / mention to ban !!"
        )
    try:
        member = await bot.get_chat(user_id)
        success = await bot.ban_chat_member(
             chat_id=chat.id,
             user_id=member.id
        )
        if success:
            member_mention = mention_html(member.id, member.first_name)
            return await message.reply_text(
text=(
f"""
<b>⚡ User {member_mention} Banned in {chat.title}.</b>
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
