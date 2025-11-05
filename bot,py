import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# === ВАШИ ДАННЫЕ ===
BOT_TOKEN = "8501908088:AAFh90gv0Og49XxZQu-vX3jjCinBsmX5ymo"
YOUR_CHAT_ID = 530132086
# === КОНЕЦ ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def handle_message(update: Update, context: CallbackContext):
    """Обрабатывает все входящие сообщения"""
    try:
        message = update.message
        
        if message.text:
            context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=f"\n\n{message.text}"
            )
            message.reply_text("✅ Ваше анонимное сообщение доставлено! Спасибо.")
            
        elif message.photo:
            photo_file = message.photo[-1].get_file()
            photo_data = photo_file.download_as_bytearray()
            
            context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=photo_data,
                caption="📷 Новое анонимное изображение"
            )
            message.reply_text("✅ Ваше анонимное изображение доставлено! Спасибо.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")

def start_command(update: Update, context: CallbackContext):
    """Команда /start"""
    welcome_text = """
👋 Привет! Я бот для отправления анонимных сообщений в Совет Управления сообществом "БУРОВИЧОК"!

📨 Просто напишите мне любое сообщение или отправьте фото - и я анонимно перешлю его в Совет Управления.

🔒 Все сообщения анонимны.
    """
    update.message.reply_text(welcome_text)

def main():
    """Запуск бота"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.all, handle_message))
    
    print("🤖 Бот запущен и готов к работе! ✅")
    print("⚡️ Работает 24/7 на Render.com")
    
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
