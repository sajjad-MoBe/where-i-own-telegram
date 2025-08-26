import asyncio
import trace
import traceback
from typing import Optional

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonRequestChat,
    ChatAdministratorRights,
)
from telegram.constants import ChatType
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = "8368343328:AAFGpjr5VDk0qvaEWm5YxXt8WkA0L-27eRA" # Replace with your bot token

START_EN = (
    "The bot helps you view channels and groups where you are the owner or an administrator, "
    "even if you have already left them.\n\n"
    "1. Select the chat type (channel or group) using the buttons.\n\n"
    "2. Click on the desired chat — the bot will send its name.\n\n"
    "If the chat doesn't open, it means the Telegram server is unable to display it, "
    "and returning to it won't be possible."
)

START_FA = (
    "این ربات به شما کمک می‌کند کانال‌ها و گروه‌هایی را که مالک یا ادمین آن‌ها بوده‌اید ببینید، "
    "حتی اگر قبلاً از آن‌ها خارج شده باشید.\n\n"
    "۱) با دکمه‌ها نوع چت (کانال یا گروه) را انتخاب کنید.\n\n"
    "۲) روی چت دلخواه بزنید — ربات نام آن را برای شما ارسال می‌کند.\n\n"
    "اگر چت باز نشد، یعنی سرور تلگرام قادر به نمایش آن نیست و برگشتن به آن امکان‌پذیر نخواهد بود."
)

def build_main_keyboard() -> ReplyKeyboardMarkup:
    btn_channels_admin = KeyboardButton(
        text="List Of Channels Where I Am An Admin",
        request_chat=KeyboardButtonRequestChat(
            request_id=101,
            chat_is_channel=True,
            user_administrator_rights=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=False,
                can_change_info=True,
                can_invite_users=True,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False,
            ),
        ),
    )

    btn_groups_admin = KeyboardButton(
        text="List Of Group Chats Where I Am An Admin",
        request_chat=KeyboardButtonRequestChat(
            request_id=102,
            chat_is_channel=False,
            user_administrator_rights=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=False,
                can_change_info=True,
                can_invite_users=True,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False,
            ),
        ),
    )

    btn_my_channels = KeyboardButton(
        text="List Of My Channels",
        request_chat=KeyboardButtonRequestChat(
            request_id=201,
            chat_is_channel=True,
            user_administrator_rights=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False,
            ),
        ),
    )

    btn_my_groups = KeyboardButton(
        text="List Of My Group Chats",
        request_chat=KeyboardButtonRequestChat(
            request_id=202,
            chat_is_channel=False,
            user_administrator_rights=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_post_stories=True,
                can_edit_stories=True,
                can_delete_stories=True,
            ),
        ),
    )

    kb = [
        [btn_channels_admin],
        [btn_groups_admin],
        [btn_my_channels],
        [btn_my_groups],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        START_EN + "\n\n---------------------------------\n\n" + START_FA,
        reply_markup=build_main_keyboard(),
        disable_web_page_preview=True,
    )

async def on_chat_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Telegram sends Message.chat_shared with the selected chat_id (and sometimes title/username).
    We then try to fetch full chat info via get_chat to get a reliable title.
    """
    if not update.message or not update.message.chat_shared:
        return

    shared = update.message.chat_shared
    chat_id = shared.chat_id

    title: Optional[str] = shared.title
    username: Optional[str] = shared.username

    try:
        chat = await context.bot.get_chat(chat_id)
        title = getattr(chat, "title", title) or getattr(chat, "full_name", title) or title
        ctype = chat.type  # ChatType.PRIVATE / GROUP / SUPERGROUP / CHANNEL
    except Exception:
        chat = None
        ctype = None 

    chat_type_str_en = {
        ChatType.PRIVATE: "private",
        ChatType.GROUP: "group",
        ChatType.SUPERGROUP: "supergroup",
        ChatType.CHANNEL: "channel",
    }.get(ctype, "chat")

    chat_type_str_fa = {
        ChatType.PRIVATE: "خصوصی",
        ChatType.GROUP: "گروه",
        ChatType.SUPERGROUP: "سوپرگروه",
        ChatType.CHANNEL: "کانال",
    }.get(ctype, "چت")

    name_part_en = f"**{title}**" if title else "(unknown title)"
    name_part_fa = f"**{title}**" if title else "(عنوان نامشخص)"

    username_part = f"\nUsername: @{username}" if username else ""

    text_en = (
        f"You shared a {chat_type_str_en} with this bot.\n"
        f"Name: {name_part_en}\nChat ID: `{chat_id}`{username_part}"
    )
    text_fa = (
        f"نام: {name_part_fa}\nشناسه چت (Chat ID): `{chat_id}`"
        + (f"\nیوزرنیم: @{username}" if username else "")
    )

    await update.message.reply_markdown(text_en + "\n\n---------------------------------\n\n" + text_fa)

async def echo_or_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "Please use the buttons below to share a chat with the bot.\n"
        "لطفاً از دکمه‌های زیر برای اشتراک‌گذاری یک چت با ربات استفاده کنید.",
        reply_markup=build_main_keyboard(),
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, on_chat_shared))
    app.add_handler(MessageHandler(filters.ALL, echo_or_help))

    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
