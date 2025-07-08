
import sqlite3
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7847661218:AAFjJ8DOpzoj0-fRGQJ1PSkCCsAB9qS8GNQ"
openai.api_key = "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"

DB_NAME = "crm_customers.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers_crm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            introduction TEXT,
            phone TEXT,
            address TEXT,
            contact_summary TEXT,
            follow_up TEXT,
            customer_value TEXT,
            customer_type TEXT,
            birth_date TEXT,
            seller_id INTEGER,
            debt_amount TEXT
        )
    ''')
    conn.commit()
    conn.close()

def parse_customer_info(message: str):
    prompt = f"""
    لطفاً از متن زیر اطلاعات مشتری را استخراج کن:
    نام کامل، نحوه آشنایی، شماره تماس، آدرس، خلاصه تماس، تاریخ پیگیری، ارزش مشتری، نوع مشتری، تاریخ تولد، مبلغ بدهی.

    پیام:
    {message}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != "vahid91640":
        await update.message.reply_text("❗ ربات فقط برای مدیر فعال است.")
        return
    await update.message.reply_text("سلام، ربات CRM بانیس آماده است. پیام‌هات رو بفرست.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    try:
        parsed = parse_customer_info(message_text)
        fields = parsed.split("\n")
        if len(fields) < 10:
            raise ValueError("اطلاعات کافی نیست.")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers_crm (
                full_name, introduction, phone, address, contact_summary,
                follow_up, customer_value, customer_type, birth_date,
                seller_id, debt_amount
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*fields[:10], user_id, fields[10] if len(fields) > 10 else "0"))
        conn.commit()
        conn.close()

        await update.message.reply_text("✅ مشتری با موفقیت ثبت شد.")
    except Exception as e:
        await update.message.reply_text(f"❗ خطا در پردازش. لطفاً اطلاعات را بررسی کنید.")

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
