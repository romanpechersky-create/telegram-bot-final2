import os
import logging
from flask import Flask, request
import requests

# === ВАШИ ДАННЫЕ ===
BOT_TOKEN = "8501908088:AAFh90gv0Og49XxZQu-vX3jjCinBsmX5ymo"
YOUR_CHAT_ID = 530132086
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
# === КОНЕЦ ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

def send_telegram_message(chat_id, text, parse_mode=None):
    """Отправляет сообщение через Telegram Bot API"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if parse_mode:
        data["parse_mode"] = parse_mode
        
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")
        return False

def send_photo(chat_id, photo_url, caption=None):
    """Отправляет фото через Telegram Bot API"""
    url = f"{TELEGRAM_API_URL}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo_url
    }
    if caption:
        data["caption"] = caption
        
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Ошибка отправки фото: {e}")
        return False

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>🤖 Анонимный бот</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>🤖 Бот для анонимных сообщений</h1>
            <p>Бот работает! ✅ Webhook версия.</p>
            <p>Используйте Telegram бота для отправки сообщений.</p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обрабатывает входящие сообщения от Telegram"""
    try:
        data = request.get_json()
        logging.info(f"Получены данные: {data}")
        
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            # Обработка команды /start
            if text == '/start':
                welcome_text = """
👋 Привет! Я бот для отправления анонимных сообщений в Совет Управления сообществом "БУРОВИЧОК"!

📨 Просто напишите мне любое сообщение - и я анонимно перешлю его в Совет Управления.

🔒 Все сообщения анонимны.
                """
                send_telegram_message(chat_id, welcome_text)
            
            # Обработка обычных текстовых сообщений
            elif text and not text.startswith('/'):
                # Пересылаем сообщение админу
                send_telegram_message(
                    YOUR_CHAT_ID, 
                    f"📨 Новое анонимное сообщение:\n\n{text}"
                )
                # Подтверждаем пользователю
                send_telegram_message(
                    chat_id, 
                    "✅ Ваше анонимное сообщение доставлено! Спасибо."
                )
            
            # Обработка фото
            elif 'photo' in message:
                # Получаем самую большую версию фото
                photos = message['photo']
                largest_photo = photos[-1]  # Последний элемент - самый большой
                file_id = largest_photo['file_id']
                
                # Получаем ссылку на файл
                file_info_url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
                file_response = requests.get(file_info_url)
                file_data = file_response.json()
                
                if file_data['ok']:
                    file_path = file_data['result']['file_path']
                    photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                    
                    # Пересылаем фото админу
                    send_photo(
                        YOUR_CHAT_ID,
                        photo_url,
                        "📷 Новое анонимное фото"
                    )
                    
                    # Подтверждаем пользователю
                    send_telegram_message(
                        chat_id,
                        "✅ Ваше анонимное изображение доставлено! Спасибо."
                    )
        
        return "OK", 200
        
    except Exception as e:
        logging.error(f"Ошибка в webhook: {e}")
        return "Error", 500

def set_webhook():
    """Устанавливает вебхук при запуске"""
    try:
        # Получаем URL приложения
        render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if render_hostname:
            webhook_url = f"https://{render_hostname}/webhook"
            
            # Устанавливаем webhook
            set_webhook_url = f"{TELEGRAM_API_URL}/setWebhook?url={webhook_url}"
            response = requests.get(set_webhook_url)
            
            if response.status_code == 200:
                logging.info(f"✅ Webhook установлен: {webhook_url}")
                print(f"✅ Webhook установлен: {webhook_url}")
            else:
                logging.error(f"❌ Ошибка установки webhook: {response.text}")
                print(f"❌ Ошибка установки webhook: {response.text}")
        else:
            logging.warning("RENDER_EXTERNAL_HOSTNAME не установлен, webhook не настроен")
            print("⚠️ RENDER_EXTERNAL_HOSTNAME не установлен, webhook не настроен")
            
    except Exception as e:
        logging.error(f"❌ Ошибка при установке webhook: {e}")
        print(f"❌ Ошибка при установке webhook: {e}")

if __name__ == '__main__':
    # Устанавливаем webhook при запуске
    set_webhook()
    
    # Запускаем Flask приложение
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
