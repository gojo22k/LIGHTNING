from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Function to trigger the upgrade menu (can be called from other files)
async def show_upgrade_menu(bot, chat_id, user_id):
    text = f"""**📦 Uᴘɢʀᴀᴅᴇ Yᴏᴜʀ 𝙿𝚕𝚊𝚗!**

**🔓 Fʀᴇᴇ 𝙿ʟᴀɴ**  
**💰 Pʀɪᴄᴇ**: **₹0 / year**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 2 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 10 GB

**🪙 Bᴀsɪᴄ 𝙿ʟᴀɴ**  
**💰 Pʀɪᴄᴇ**: **₹19 / week**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 50 GB

**⚡ Sᴛᴀɴᴅᴀʀᴅ 𝙿ʟᴀɴ**  
**💰 Pʀɪᴄᴇ**: **₹49 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 100 GB

**💎 Pʀᴏ 𝙿ʟᴀɴ**  
**💰 Pʀɪᴄᴇ**: **₹499 / year**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: ♾️ Unlimited

🔹 **Pᴀʏᴍᴇɴᴛ Iɴsᴛʀᴜᴄᴛɪᴏɴs**  
Pay using UPI ID: `rasanandamohapatra2014@okhdfcbank`  
After payment, send screenshots of the transaction and your ID `{user_id}` to Admin: [@AniflixAnkit](https://t.me/AniflixAnkit)

📩 **Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ ғᴏʀ Assɪsᴛᴀɴᴄᴇ**  
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact Admin", url="https://t.me/AniflixAnkit")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    
    await bot.send_message(chat_id, text=text, reply_markup=keyboard)

# Command to display the upgrade menu
@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot, message):
    user_id = message.from_user.id  # Fetch the user ID from the message
    await show_upgrade_menu(bot, message.chat.id, user_id)