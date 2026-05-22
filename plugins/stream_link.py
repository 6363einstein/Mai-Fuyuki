"""
stream_link.py
User forwards/sends any file to bot in PM
→ Bot saves to BIN_CHANNEL
→ Generates Watch Online + Download links from Render server
→ Sends buttons back to user
"""

import logging
import asyncio
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from info import URL, BIN_CHANNEL, LOG_CHANNEL, DELETE_TIME
from dreamxbotz.util.file_properties import get_name, get_hash
from utils import get_size

logger = logging.getLogger(__name__)


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

    # Get media object
    media = (
        message.video
        or message.audio
        or message.document
        or message.video_note
        or message.voice
    )
    if not media:
        return

    processing = await message.reply(
        "⏳ Please wait, generating links...",
        quote=True
    )

    try:
        # Save to BIN_CHANNEL to get stable message ID + hash
        log_msg = await client.forward_messages(
            chat_id=BIN_CHANNEL,
            from_chat_id=message.chat.id,
            message_ids=message.id
        )

        file_name    = get_name(log_msg)
        fname_quoted = quote_plus(file_name)
        fhash        = get_hash(log_msg)
        mid          = str(log_msg.id)

        # Build URLs using Render server
        stream_url   = f"{URL}watch/{mid}/{fname_quoted}?hash={fhash}"
        download_url = f"{URL}{mid}/{fname_quoted}?hash={fhash}"

        # File size
        size = ""
        if hasattr(media, "file_size") and media.file_size:
            size = get_size(media.file_size)

        caption = (
            f"<b>{file_name}</b>"
            + (f"\n<code>{size}</code>" if size else "")
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

        # Log to LOG_CHANNEL
        user    = message.from_user
        mention = user.mention if user else "Unknown"
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f"🔗 <b>Stream link generated</b>\n"
                f"👤 User: {mention} (<code>{user.id if user else '?'}</code>)\n"
                f"📁 File: <code>{file_name}</code>"
                + (f"\n📦 Size: {size}" if size else "")
            ),
            parse_mode="html",
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.exception(f"stream_link error: {e}")
        try:
            await processing.edit_text(
                "⚠️ Could not generate links.\n"
                "Make sure <code>FQDN</code> is set correctly in Render environment variables.",
                parse_mode="html"
            )
        except Exception:
            pass
