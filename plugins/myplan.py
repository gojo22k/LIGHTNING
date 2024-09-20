import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import Database
from helper.progress import humanbytes
from helper.date import check_expi
from datetime import datetime, date as date_
from config import Config

import logging

# Create an instance of Database
db = Database(uri=Config.DB_URL, database_name=Config.DB_NAME)

@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    logging.debug("Received /myplan command")
    
    try:
        used_ = await db.find_one(message.from_user.id)
        if not used_:
            await message.reply("No data found for your user ID.")
            logging.warning(f"No data found for user ID: {message.from_user.id}")
            return
        
        logging.debug(f"User data: {used_}")

        daily = used_["daily"]
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            await db.daily(message.from_user.id, epcho)
            await db.used_limit(message.from_user.id, 0)
        
        _newus = await db.find_one(message.from_user.id)
        used = _newus["used_limit"]
        limit = _newus["uploadlimit"]
        remain = int(limit) - int(used)
        user = _newus["usertype"]
        ends = _newus["prexdate"]
        
        if ends:
            pre_check = check_expi(ends)
            if not pre_check:
                await db.uploadlimit(message.from_user.id, 2147483652)
                await db.usertype(message.from_user.id, "Free")
        
        if ends is None:
            text = f"**User ID :** `{message.from_user.id}` \n**Name :** {message.from_user.mention} \n\n**🏷 Plan :** {user} \n\n✓ Upload 2GB Files \n✓ Daily Upload : {humanbytes(limit)} \n✓ Today Used : {humanbytes(used)} \n✓ Remain : {humanbytes(remain)} \n✓ Timeout : 2 Minutes \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n**Validity :** Lifetime"
        else:
            normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
            text = f"**User ID :** `{message.from_user.id}` \n**Name :** {message.from_user.mention} \n\n**🏷 Plan :** {user} \n\n✓ High Priority \n✓ Upload 4GB Files \n✓ Daily Upload : {humanbytes(limit)} \n✓ Today Used : {humanbytes(used)} \n✓ Remain : {humanbytes(remain)} \n✓ Timeout : 0 Second \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n**Your Plan Ends On :** {normal_date}"
        
        if user == "Free":
            await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
        else:
            await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Cancel ✖️", callback_data="cancel")]]))
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await message.reply("An error occurred while processing your request.")
