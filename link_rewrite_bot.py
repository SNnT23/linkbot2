#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)

# ပြောင်းချင်တဲ့ bot username တွေ
OLD_BOT = os.getenv("OLD_BOT", "sender_RMC_bot").lstrip("@")
NEW_BOT = os.getenv("NEW_BOT", "RMC_Delivery_Servicebot").lstrip("@")

# t.me/<oldbot>?start=xxxx  ကိုသာ target လုပ်
PATTERN = re.compile(
    rf"(https?://t\.me/){re.escape(OLD_BOT)}(\?start=[^\s]+)",
    re.IGNORECASE
)

def rewrite(text: str) -> str:
    return PATTERN.sub(rf"\1{NEW_BOT}\2", text)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me your t.me links and I’ll rewrite them.\n"
        f"Replacing: {OLD_BOT} → {NEW_BOT}"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Just send text containing links like:\n"
        f"https://t.me/{OLD_BOT}?start=...\n"
        "I will reply with the rewritten version."
    )

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    out = rewrite(text)
    if out == text:
        await update.message.reply_text("No matching links found to rewrite.")
    else:
        await update.message.reply_text(out)

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Missing BOT_TOKEN env var. Set it from @BotFather token.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
