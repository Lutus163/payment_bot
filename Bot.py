import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
import logging


TOKEN = '6779027788:AAGrfHq5F11bvIfW0Gnw6uGpZ9xAr6pVI_k'
bot = telebot.TeleBot(TOKEN)
OWNER_CHAT_ID = 1194493488


@bot.message_handler(commands=['start'])
def start(message):
    with open('/tg_bot/img/start.png', 'rb') as photo:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Оплата")
        keyboard.add(button)
        bot.send_photo(message.chat.id, photo=photo, caption='Стоимость:\n5555р\n5000р и скрин репоста от тебя🙏🏻\n13332р на троих (приводи 2-х друзей и оплачивайте одним чеком)\n\nПрисоединиться вы можете в любой день, доступ к записи практики будет у вас в течении 90 дней!\n\nДля оплаты отправьте сообщение нажмите на кнопку «Оплата»', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() == 'оплата')
def handle_payment(message):
    bot.send_message(message.chat.id, 'Как оплатить?👇🏻\nТ-Банк: 2200700402852221\n\nКаспи Казахстан: 4400430276906358\n\nПосле оплаты отправьте сюда скриншот с переводом🙏🏻')

# Настройка логирования
logging.basicConfig(level=logging.INFO)



def start_bot():
    try:
        @bot.message_handler(commands=['start'])
        def start(message):
            with open('img/start.png', 'rb') as photo:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button = types.KeyboardButton("Оплата")
                keyboard.add(button)
                bot.send_photo(message.chat.id, photo=photo, caption='Стоимость:\n5555р\n5000р и скрин репоста от тебя🙏🏻\n13332р на троих (приводи 2-х друзей и оплачивайте одним чеком)\n\nПрисоединиться вы можете в любой день, доступ к записи практики будет у вас в течении 90 дней!\n\nДля оплаты отправьте сообщение нажмите на кнопку «Оплата»', reply_markup=keyboard)

        @bot.message_handler(func=lambda message: message.text.lower() == 'оплата')
        def handle_payment(message):
            bot.send_message(message.chat.id, 'Как оплатить?👇🏻\nТ-Банк: 2200700402852221\n\nКаспи Казахстан: 4400430276906358\n\nПосле оплаты отправьте сюда скриншот с переводом🙏🏻')

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
        bot.polling(none_stop=True)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        time.sleep(5)  # Задержка перед перезапуском
        start_bot()  # Перезапуск бота

if __name__ == '__main__':
    start_bot()

