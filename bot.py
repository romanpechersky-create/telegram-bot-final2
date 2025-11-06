import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

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

# Создаем Application
application = Application.builder().token(BOT_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает все входящие сообщения"""
    try:
        message = update.message
        
        if message.text:
            await context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=f"📨 Новое анонимное сообщение:\n\n{message.text}"
            )
            await message.reply_text("✅ Ваше анонимное сообщение доставлено! Спасибо.")
            
        elif message.photo:
            # Получаем самую большую версию фото
            photo_file = await message.photo[-1].get_file()
            # Скачиваем фото как bytes
            photo_bytes = await photo_file.download_as_bytearray()
            
            await context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=photo_bytes,
                caption="📷 Новое анонимное фото"
            )
            await message.reply_text("✅ Ваше анонимное изображение доставлено! Спасибо.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply_text("❌ Произошла ошибка при обработке сообщения.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    welcome_text = """
👋 Привет! Я бот для отправления анонимных сообщений в Совет Управления сообществом "БУРОВИЧОК"!

📨 Просто напишите мне любое сообщение или отправьте изображение - и я анонимно перешлю его в Совет Управления.

🔒 Все сообщения анонимны.
    """
    await update.message.reply_text(welcome_text)

# Добавляем обработчики
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

@app.route('/')
def home():
    return "🤖 Бот работает! ✅ Webhook версия."

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Эндпоинт для вебхуков от Telegram"""
    try:
        # Получаем данные от Telegram
        json_data = request.get_json()
        
        # Создаем объект Update из JSON
        update = Update.de_json(json_data, application.bot)
        
        # Обрабатываем обновление
        await application.process_update(update)
        
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка в webhook: {e}")
        return "Error", 500

async def set_webhook():
    """Устанавливает вебхук при запуске"""
    try:
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        await application.bot.set_webhook(webhook_url)
        logging.info(f"Webhook установлен: {webhook_url}")
        print(f"✅ Webhook установлен: {webhook_url}")
    except Exception as e:
        logging.error(f"Ошибка установки webhook: {e}")
        print(f"❌ Ошибка установки webhook: {e}")

def main():
    """Основная функция запуска"""
    # Устанавливаем вебхук
    application.run_polling()
    
    # Запускаем Flask приложение
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    # Запускаем установку webhook и сервер
    import asyncio
    asyncio.run(set_webhook())
    main()
