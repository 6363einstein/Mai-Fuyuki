# Stream & Download link generator
# When user sends a file to bot in PM → bot generates stream + download buttons

import logging
import asyncio
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from info import URL, BIN_CHANNEL, LOG_CHANNEL, DELETE_TIME, ADMINS
from dreamxbotz.util.file_properties import get_name, get_hash
from utils import get_size

logger = logging.getLogger(__name__)

SUPPORTED_MEDIA = (
    "video", "audio", "document",
    "video_note", "voice"
)


def get_media(message: Message):
    """Return the media object from any supported message type."""
    for attr in SUPPORTED_MEDIA:
        media = getattr(message, attr, None)
        if media:
            return media, attr
    return None, None


@Client.on_message(
    filters.private
    & filters.incoming
    & (
        filters.video
        | filters.audio
        | filters.document
        | filters.video_note
        | filters.voice
    )
)
async def generate_stream_link(client, message: Message):
    """
    User sends a file in PM →
    Bot uploads it to BIN_CHANNEL →
    Generates stream + download links from render server →
    Sends buttons back to user.
    """
    media, media_type = get_media(message)
    if not media:
        return

    processing = await message.reply(
        "⏳ Generating links, please wait...",
        quote=True
    )

    try:
        # Forward file to BIN_CHANNEL to get a stable message ID + hash
        # Forward to BIN_CHANNEL for stream link generation
        log_msg = await client.forward_messages(
            chat_id=BIN_CHANNEL,
            from_chat_id=message.chat.id,
            message_ids=message.id
        )

        # Also forward to LOG_CHANNEL for admin record
        await client.forward_messages(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_ids=message.id
        )

        file_name  = quote_plus(get_name(log_msg))
        file_hash  = get_hash(log_msg)
        msg_id     = str(log_msg.id)

        stream_url   = f"{URL}watch/{msg_id}/{file_name}?hash={file_hash}"
        download_url = f"{URL}{msg_id}/{file_name}?hash={file_hash}"

        size = get_size(media.file_size) if hasattr(media, "file_size") else ""
        size_text = f"  •  {size}" if size else ""

        caption = (
            f"<b>🎬 Stream & Download Links</b>\n\n"
            f"<code>{get_name(log_msg)}</code>{size_text}\n\n"
            f"<i>Links expire after the file is removed.</i>"
        )

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("▶️ Watch Online", url=stream_url),
                InlineKeyboardButton("⬇️ Download", url=download_url),
            ]
        ])

        await processing.delete()
        await message.reply(
            text=caption,
            quote=True,
            reply_markup=buttons,
            parse_mode="html",
            disable_web_page_preview=True
        )

        # Log to BIN_CHANNEL with user info
        user = message.from_user
        mention = user.mention if user else "Unknown"
        await log_msg.reply(
            f"🔗 Link generated\n"
            f"👤 User: {mention} (<code>{user.id if user else '?'}</code>)\n"
            f"📁 File: {get_name(log_msg)}",
            quote=True,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.exception(f"stream_link error: {e}")
        await processing.edit_text(
            "⚠️ Could not generate links. Make sure the bot is admin in BIN_CHANNEL."
        )
