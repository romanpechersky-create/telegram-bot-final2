import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === ВАШИ ДАННЫЕ ===
BOT_TOKEN = "8501908088:AAFh90gv0Og49XxZQu-vX3jjCinBsmX5ymo"
YOUR_CHAT_ID = 530132086
# === КОНЕЦ ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает все входящие сообщения"""
    try:
        message = update.message
        
        if message.text:
            await context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=f"\n\n{message.text}"
            )
            await message.reply_text("✅ Ваше анонимное сообщение доставлено! Спасибо.")
            
        elif message.photo:
            photo_file = await message.photo[-1].get_file()
            photo_data = await photo_file.download_as_bytearray()
            
            await context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=photo_data,
                caption="📷 Новое анонимное фото"
            )
            await message.reply_text("✅ Ваше анонимное изображение доставлено! Спасибо.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    welcome_text = """
👋 Привет! Я бот для отправления анонимных сообщений в Совет Управления сообществом "БУРОВИЧОК"!

📨 Просто напишите мне любое сообщение или отправьте изображение - и я анонимно перешлю его в Совет Управления.

🔒 Все сообщения анонимны.
    """
    await update.message.reply_text(welcome_text)

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(MessageHandler(filters.COMMAND, start_command))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен и готов к работе! ✅")
    print("⚡ Работает 24/7 на Render.com")
    
    application.run_polling()

if __name__ == '__main__':
    main()
