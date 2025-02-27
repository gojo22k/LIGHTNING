import re
import os
import time
from os import environ

# Shortlink API configuration
API = environ.get("API", "81aa9734c37474fbc63b3dcb719eaf14ecd8f27f") # shortlink api
URL = environ.get("URL", "ziplinker.net") # shortlink domain without https://
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "https://t me/MisterBrutal") # how to open link 
BOT_USERNAME = environ.get("BOT_USERNAME", "FastFileRenamer4GBot") # bot username without @
VERIFY = False  # Convert string to boolean

id_pattern = re.compile(r'^.\d+$')

class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "25198711")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "2a99a1375e26295626c04b4606f72752")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7066960405:AAHXNR-eSyYbJt7BHlriY0g9chDWpfIE0Do")  # ⚠️ Required
    
    # premium 4g renaming client
    STRING_API_ID = os.environ.get("STRING_API_ID", "")
    STRING_API_HASH = os.environ.get("STRING_API_HASH", "")
    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    # database config
    DB_URL = environ.get("DB_URL", "mongodb+srv://Api:Api123@api.m67v6.mongodb.net/?retryWrites=true&w=majority&appName=Api")
    DB_NAME = environ.get("DB_NAME", "Api")  # ⚠️ Required

    # other configs
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", "https://iili.io/39xn6H7.md.jpg")
    ADMIN = [int(admin) if id_pattern.search(
        admin) else admin for admin in os.environ.get('ADMIN', '1740287480').split()]  # ⚠️ Required
    
    FORCE_SUB = os.environ.get("FORCE_SUB", "Aniflix_Official") # ⚠️ Required Username without @
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002219568827"))  # ⚠️ Required
    FLOOD = int(os.environ.get("FLOOD", '105'))
    BANNED_USERS = set(int(x) for x in os.environ.get(
        "BANNED_USERS", "1234567890").split())

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))

    # Add the missing attributes
    VERIFY = VERIFY
    BOT_USERNAME = BOT_USERNAME
    VERIFY_TUTORIAL = VERIFY_TUTORIAL


class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hᴇʟʟᴏ 👋 {}!</b>\n\n
◈ I Cᴀɴ Rᴇɴᴀᴍᴇ Fɪʟᴇs ᴜᴘᴛᴏ 4GB, 
ᴛʜɪꜱ ɪꜱ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ʀᴇɴᴀᴍᴇ ʙᴏᴛ ᴡɪᴛʜ ʟᴀᴛᴇꜱᴛ ꜰᴇᴀᴛᴜʀᴇꜱ.\n\n
➙ ᴛʜɪꜱ ʙᴏᴛ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ꜱᴄʀᴇᴇɴꜱʜᴏᴛs ᴀɴᴅ ꜱᴀᴍᴘʟᴇ ᴠɪᴅᴇᴏs ꜰʀᴏᴍ ʏᴏᴜʀ ꜰɪʟᴇ.\n
➙ ʏᴏᴜ ᴄᴀɴ ʀᴇɴᴀᴍᴇ ꜰɪʟᴇs, sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟs, ᴀɴᴅ sᴇᴛ ᴄᴀᴘᴛɪᴏɴs ᴏꜰ ꜰɪʟᴇs, ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ.\n\n
<a href="YOUR_CHANNEL_POST_URL"><b>Read More Commands</b></a>
"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 Mʏ Nᴀᴍᴇ : {}
├👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/AniflixAnkit>ANKIT</a>
├👑 Iɴsᴛᴀɢʀᴀᴍ : <a href=https://www.instagram.com/gojo22k>Iɴsᴛᴀɢʀᴀᴍ</a> 
├📕 Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Lᴀɴɢᴜᴀɢᴇ: <a href=https://www.python.org>Pyᴛʜᴏɴ 3</a>
├💾 Dᴀᴛᴀ Bᴀꜱᴇ: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
╰───────────────⍟ """

    HELP_TXT = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
  
<b>•></b> /start Tʜᴇ Bᴏᴛ Aɴᴅ Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.


📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
Exᴀᴍᴩʟᴇ:- <code> /set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration} </code>

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nɴᴀᴍᴇ \nAɴᴅ Aᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           


<b>⦿ Dᴇᴠᴇʟᴏᴘᴇʀ:</b> <a href=https://t.me/aniflixClou> Ankit 😎</a>
"""

    SEND_METADATA = """
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @aniflixClou" -metadata author="@aniflixClou" -metadata:s:s title="Subtitled By :- @aniflixClou" -metadata:s:a title="By :- @aniflixClou" -metadata:s:v title="By:- @aniflixClou" </code>

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @aniflixClou
"""
    PROGRESS_BAR = """<b>\n
╭━━❰Aɴᴋɪᴛ Rᴇɴᴀᴍɪɴɢ Rᴇᴘᴏʀᴛ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ ᴇᴛᴀ: {4}
┣⪼ 🔥 Bᴏᴛ Bʏ: @AniflixAnkit
╰━━━━━━━━━━━━━━━━━━━➣

<b>⦿ Channel:</b> <a href=https://t.me/Aniflix_Official> 
🅰🅽🅸🅵🅻🅸🆇 😎</a>
</b>"""
