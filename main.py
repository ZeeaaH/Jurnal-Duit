import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import database
import gemini_helper

load_dotenv()
database.init_db()

async def catat_keuangan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        data = gemini_helper.ekstrak_transaksi(user_text)
        
        database.simpan_transaksi(
            data['tipe'],
            data['kategori'],
            data['nominal'],
            data['keterangan']
        )
        
        reply = (
            f"✅ **Transaksi Berhasil Dicatat!**\n\n"
            f"📌 **Tipe:** {data['tipe'].capitalize()}\n"
            f"🏷 **Kategori:** {data['kategori'].capitalize()}\n"
            f"💰 **Nominal:** Rp{data['nominal']:,}\n"
            f"📝 **Keterangan:** {data['keterangan']}"
        )
    except Exception as e:
        print(f"[ERROR]: {e}")
        reply = f"❌ Gagal memproses catatan.\n\n`Detail: {e}`"

    await update.message.reply_text(reply, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, catat_keuangan))
    app.run_polling()