from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7847661218:AAFjJ8DOpzoj0-fRGQJ1PSkCCsAB9qS8GNQ"
ADMIN_USERNAME = "vahid91640"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username == ADMIN_USERNAME:
        await update.message.reply_text("ربات برای مدیر فعال است.")
    else:
        await update.message.reply_text("سلام! ربات فعال است.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()