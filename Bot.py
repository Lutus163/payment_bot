import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
from threading import Thread


TOKEN = '7969372334:AAEeniSBTLUMhkfzueRS8Az938UFxTb1Ry8'
bot = telebot.TeleBot(TOKEN)
OWNER_CHAT_ID = 1194493488

@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('img/join.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo=photo, caption='ИНСТРУКЦИЯ С РЕКВИЗИТАМИ')

@bot.message_handler(func=lambda message: message.text == "Оплата")
def handle_payment_message(message):
    bot.reply_to(message, 'Пожалуйста, отправьте фото скриншота оплаты.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Проверяем, является ли это сообщением, на которое бот должен реагировать
    if message.reply_to_message and message.reply_to_message.text == 'Пожалуйста, отправьте фото скриншота оплаты.':
        try:
            file_info = bot.get_file(message.photo[-1].file_id)  # Берем максимальное качество фото
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Отправляем фото владельцу
            bot.send_photo(OWNER_CHAT_ID, downloaded_file)

            # Подтверждение для пользователя
            bot.reply_to(message, 'Скриншот был отправлен владельцу, ожидайте подтверждения.')
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            bot.reply_to(message, 'Произошла ошибка при отправке скриншота. Попробуйте ещё раз.')  


 

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

