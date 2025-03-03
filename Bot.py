import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
from threading import Thread


TOKEN = '7969372334:AAEeniSBTLUMhkfzueRS8Az938UFxTb1Ry8'
bot = telebot.TeleBot(TOKEN)





# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):



    with open('img/join.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo, caption='РЕКВИЗИТЫ', reply_markup=keyboard)



    #if message.text.lower() == "оплатить":
        #bot.send_message(message.chat.id, "Нажмите на кнопку ниже для перехода к оплате.", reply_markup=webAppKeyboard())


        

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

