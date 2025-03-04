import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
from threading import Thread


TOKEN = '7969372334:AAEeniSBTLUMhkfzueRS8Az938UFxTb1Ry8'
bot = telebot.TeleBot(TOKEN)
OWNER_CHAT_ID = 1194493488

@bot.message_handler(commands=['start'])
def start(message):
    with open('img/start.png', 'rb') as photo:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Оплата")
        keyboard.add(button)
        bot.send_photo(message.chat.id, photo=photo, caption='ПОДРОБНОСТИ:\n🫶Старт 20.03\n🫶Ежедневно с 19:00-20:30 по Москве\n🫶Трансляция в Zoom\n\nСтоимость:\n5555р\n5000р и репост марафона скрином от тебя🙏🏻\n13332р на троих (приводи 2-х друзей и оплачивайте одним чеком)\n\nПрисоединиться вы можете в любой день, доступ к записи практики будет у вас в течении 90 дней!\n\nДля оплаты отправьте сообщение "Оплата" или нажмите на кнопку.', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() == 'оплата')
def handle_payment(message):
    bot.send_message(message.chat.id, 'Как оплатить?👇🏻\nТ-Банк: 2200700402852221\n\nПосле оплаты отправьте сюда скриншот с переводом.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Формируем информацию об отправителе
    sender_info = f'Отправитель: @{message.from_user.username}\n' \
                  f'Имя: {message.from_user.first_name} {message.from_user.last_name}\n' \
                  f'ID: {message.from_user.id}'

    # Отправляем фото и информацию владельцу
    bot.send_photo(OWNER_CHAT_ID, downloaded_file, caption=sender_info)
    bot.send_message(message.chat.id, 'Ваш скриншот об оплате был отправлен, ожидайте подтверждения.')



 

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

