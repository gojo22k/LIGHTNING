from config import Config
from helper.database import Database
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio
from datetime import datetime, timedelta

db = Database(Config.DB_URL, Config.DB_NAME)

@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")

@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, message: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{message.from_user.mention} has started a broadcast.")
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    status_message = await message.reply_text("Broadcast started...!")

    done = 0
    failed = 0
    success = 0
    total_users = len(all_users)

    for user in all_users:
        try:
            await broadcast_msg.forward(chat_id=user['_id'])
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.seconds)
            await broadcast_msg.forward(chat_id=user['_id'])
            success += 1
        except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
            await db.delete_user(user['_id'])  # Delete user if account is deactivated or blocked
            failed += 1
        except Exception as e:
            failed += 1
        done += 1

        if not done % 20:
            await status_message.edit(f"Broadcast in progress:\nTotal users: {total_users}\nCompleted: {done}/{total_users}\nSuccess: {success}\nFailed: {failed}")

    await status_message.edit(f"Broadcast completed:\nTotal users: {total_users}\nCompleted: {done}/{total_users}\nSuccess: {success}\nFailed: {failed}")

pending_premium_updates = {}

@Client.on_message(filters.private & filters.user(Config.ADMIN) & filters.command(["addpremium"]))
async def add_premium(bot, message: Message):
    try:
        command_args = message.text.split()
        if len(command_args) == 2:
            user_id = int(command_args[1])

            if user_id in pending_premium_updates or await db.get_user_subscription(user_id):
                await message.reply_text("User is already in the premium list or already has a subscription.", quote=True)
                return

            pending_premium_updates[message.chat.id] = user_id

            await message.reply_text(
                "🦋 Select Plan To Upgrade.....",
                quote=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🆓 Trial (1 Day)", callback_data="trial")],
                    [InlineKeyboardButton("🪙 Basic (1 Week)", callback_data="basic")],
                    [InlineKeyboardButton("⚡ Standard (1 Month)", callback_data="standard")],
                    [InlineKeyboardButton("🚀 Advanced (2 Month)", callback_data="advanced")],
                    [InlineKeyboardButton("💎 Premium (3 Months)", callback_data="premium")],
                    [InlineKeyboardButton("🏅 Elite (6 Months)", callback_data="elite")],
                    [InlineKeyboardButton("🎖️ Ultimate (1 Year)", callback_data="ultimate")],
                    [InlineKeyboardButton("✖️ Cancel ✖️", callback_data="cancel")]
                ])
            )
        else:
            await message.reply_text("Please use the command like `/addpremium {user_id}`", quote=True)
    except Exception as e:
        await message.reply_text(f"Error: {e}", quote=True)

def calculate_validity(plan_type):
    now = datetime.now()
    if plan_type == "trial":
        return now + timedelta(days=1)
    elif plan_type == "basic":
        return now + timedelta(weeks=1)
    elif plan_type == "standard":
        return now + timedelta(days=30)
    elif plan_type == "advanced":
        return now + timedelta(days=60)  # 1 Month
    elif plan_type == "premium":
        return now + timedelta(days=90)  # 3 Months
    elif plan_type == "elite":
        return now + timedelta(days=180)  # 6 Months
    elif plan_type == "ultimate":
        return now + timedelta(days=365)  # 1 Year
    return now

@Client.on_callback_query(filters.regex('trial|basic|standard|advanced|premium|elite|ultimate'))
async def upgrade_plan(bot, update):
    try:
        plan_type = update.data
        admin_id = update.message.chat.id

        if admin_id in pending_premium_updates:
            user_id = pending_premium_updates[admin_id]
            validity_end = calculate_validity(plan_type)
            plan_name = {
                "trial": "🆓 Trial",
                "basic": "🪙 Basic",
                "standard": "⚡ Standard",
                "advanced": "🚀 Advanced",
                "premium": "💎 Premium",
                "elite": "🏅 Elite",
                "ultimate": "🎖️ Ultimate"
            }[plan_type]

            await db.update_user_subscription(user_id, plan_name, validity_end)
            await update.message.edit_text(f"User {user_id} upgraded to {plan_name} plan successfully.")
            await bot.send_message(user_id, f"Hey! You are now upgraded to {plan_name} plan. Check your plan with /myplan")
            del pending_premium_updates[admin_id]
        else:
            await update.message.edit_text("No user selected for upgrade.")
    except Exception as e:
        await update.message.edit_text(f"Error: {e}")

@Client.on_callback_query(filters.regex('cancel'))
async def cancel_upgrade(bot, update):
    try:
        admin_id = update.message.chat.id
        if admin_id in pending_premium_updates:
            del pending_premium_updates[admin_id]
        await update.message.edit_text("Premium upgrade canceled.")
    except Exception as e:
        await update.message.edit_text(f"Error: {e}")

@Client.on_message(filters.command("ulist") & filters.user(Config.ADMIN))
async def premium_user_list(bot: Client, message: Message):
    try:
        premium_users = await db.get_premium_users()
        now = datetime.now()
        active_premium_users = []

        for user in premium_users:
            user_id = user.get('_id')
            plan = user.get('plan', 'Non-Premium')
            validity_end = user.get('validity_end')

            if plan != 'Non-Premium' and validity_end and validity_end >= now:
                active_premium_users.append(user)

        if active_premium_users:
            premium_list = "\n".join([
                f"**User ID:** `{user['_id']}` - **Plan:** {user.get('plan', 'Unknown')} - "
                f"**Validity End:** {user.get('validity_end').strftime('%Y-%m-%d %H:%M:%S') if user.get('validity_end') else 'Unknown'}"
                for user in active_premium_users
            ])
            response_text = f"**Premium Users:**\n{premium_list}"
        else:
            response_text = "No active premium users found."

        await message.reply_text(response_text, quote=True)
    
    except Exception as e:
        await message.reply_text("An error occurred while fetching the premium user list.", quote=True)

@Client.on_message(filters.command(["removepremium"]) & filters.user(Config.ADMIN))
async def remove_premium(bot: Client, message: Message):
    try:
        command_args = message.text.split()
        if len(command_args) == 2:
            user_id = int(command_args[1])

            result = await db.delete_user(user_id)

            if result is None:
                await message.reply_text(f"User {user_id} removed from the premium list.", quote=True)
            elif result.deleted_count > 0:
                await message.reply_text(f"User {user_id} removed from the premium list.", quote=True)
                await bot.send_message(user_id, "Your premium subscription has been removed. Please upgrade to continue accessing premium features.")
            else:
                await message.reply_text(f"Error: Failed to remove user {user_id} from the premium list.", quote=True)
        else:
            await message.reply_text("Please use the command like `/removepremium {user_id}`", quote=True)
    except Exception as e:
        await message.reply_text(f"Error: {e}", quote=True)

@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(bot, message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user_subscription(user_id)
        if user and user['plan'] != 'Non-Premium':
            plan = user['plan']
            validity_end = user['validity_end'].strftime('%d-%m-%Y %H:%M:%S')
            await message.reply_text(f"Your Plan: {plan}\nValidity Ends On: {validity_end}", quote=True)
        else:
            await message.reply_text("You are not subscribed to any premium plan.", quote=True)
    except Exception as e:
        await message.reply_text(f"Error: {e}", quote=True)
