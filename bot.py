import logging
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

# === ВАШИ ДАННЫЕ ===
BOT_TOKEN = "8501908088:AAFh90gv0Og49XxZQu-vX3jjCinBsmX5ymo"
YOUR_CHAT_ID = 530132086
# === КОНЕЦ ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

# Создаем бота
bot = Bot(token=BOT_TOKEN)

def handle_message(update: Update, context: CallbackContext):
    """Обрабатывает все входящие сообщения"""
    try:
        message = update.message
        
        if message.text:
            context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=f"📨 Новое анонимное сообщение:\n\n{message.text}"
            )
            message.reply_text("✅ Ваше анонимное сообщение доставлено! Спасибо.")
            
        elif message.photo:
            photo_file = message.photo[-1].get_file()
            photo_data = photo_file.download_as_bytearray()
            
            context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=photo_data,
                caption="📷 Новое анонимное фото"
            )
            message.reply_text("✅ Ваше анонимное изображение доставлено! Спасибо.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")

def start_command(update: Update, context: CallbackContext):
    """Команда /start"""
    welcome_text = """
👋 Привет! Я бот для отправления анонимных сообщений в Совет Управления сообществом "БУРОВИЧОК"!

📨 Просто напишите мне любое сообщение или отправьте изображение - и я анонимно перешлю его в Совет Управления.

🔒 Все сообщения анонимны.
    """
    update.message.reply_text(welcome_text)

@app.route('/')
def home():
    return "🤖 Бот работает! ✅ Webhook версия."

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Эндпоинт для вебхуков от Telegram"""
    try:
        # Создаем updater для обработки обновлений
        updater = Updater(bot=bot, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчики
        dispatcher.add_handler(CommandHandler("start", start_command))
        dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_message))
        
        # Обрабатываем обновление
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
        
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка в webhook: {e}")
        return "Error", 500

def set_webhook():
    """Устанавливает вебхук при запуске"""
    try:
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        bot.set_webhook(webhook_url)
        logging.info(f"Webhook установлен: {webhook_url}")
        print(f"✅ Webhook установлен: {webhook_url}")
    except Exception as e:
        logging.error(f"Ошибка установки webhook: {e}")
        print(f"❌ Ошибка установки webhook: {e}")

if __name__ == '__main__':
    # Устанавливаем вебхук при запуске
    set_webhook()
    
    # Запускаем Flask приложение
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
