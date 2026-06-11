def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Missing BOT_TOKEN env var. Set it from @BotFather token.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    # Koyeb ရဲ့ background port handling အတွက် dummy server ပုံစံလေး လုပ်ပေးတာပါ
    # (Koyeb မှာ Error မတက်ဘဲ အမြဲ Run နေစေဖို့ ဖြစ်ပါတယ်)
    import threading
    import http.server
    import socketserver

    def run_dummy_server():
        port = int(os.getenv("PORT", 8000))
        handler = http.server.SimpleHTTPRequestHandler
        # Port ဖွင့်ရုံသက်သက်မို့လို့ log တွေကို ပိတ်ထားပါမယ်
        handler.log_message = lambda *args: None
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()

    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Bot စတင်ပတ်မောင်းခြင်း
    app.run_polling(allowed_updates=Update.ALL_TYPES)
