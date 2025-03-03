import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
from threading import Thread


TOKEN = '7969372334:AAEeniSBTLUMhkfzueRS8Az938UFxTb1Ry8'
bot = telebot.TeleBot(TOKEN)
subscribers = set()


user_requests = {}

REQUEST_LIMIT = 15 
TIME_FRAME = 10  




# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вы подписались на рассылку! Используйте команду /stop для отмены.")
    subscribers.add(chat_id)
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка на превышение лимита запросов
    if user_id in user_requests:
        request_times = user_requests[user_id]
        # Удаляем старые запросы
        request_times = [t for t in request_times if current_time - t < TIME_FRAME]
        user_requests[user_id] = request_times

        if len(request_times) >= REQUEST_LIMIT:
            bot.send_message(message.chat.id, "Слишком много запросов! Пожалуйста, подождите.")
            return

        request_times.append(current_time)
    else:
        user_requests[user_id] = [current_time]

    # Получение никнейма пользователя
    username = message.from_user.username if message.from_user.username else "пользователь"
    
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Оплатить")
    keyboard.add(button1)

    # Приветственное сообщение
    with open('img/join.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo, caption='Для оплаты отправьте сообщение "Оплатить"', reply_markup=keyboard)



# Обработчик нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    username = message.from_user.first_name
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка на превышение лимита запросов
    if user_id in user_requests:
        request_times = user_requests[user_id]
        # Удаляем старые запросы
        request_times = [t for t in request_times if current_time - t < TIME_FRAME]
        user_requests[user_id] = request_times

        if len(request_times) >= REQUEST_LIMIT:
            bot.answer_callback_query(id, "Слишком много запросов! Пожалуйста, подождите.")
            return

        request_times.append(current_time)
    else:
        user_requests[user_id] = [current_time]



    if message.text.lower() == "оплатить":
        def webAppKeyboard():
            keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
            webApp = types.WebAppInfo("https://payform.ru/ku3hNIm") #создаем webappinfo - формат хранения url
            payment = types.KeyboardButton(text="Оплата", web_app=webApp) #создаем кнопку типа webapp
            keyboard.add(payment) #добавляем кнопки в клавиатуру
            return keyboard
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже для перехода к оплате.", reply_markup=webAppKeyboard())


        

def send_periodic_messages():
    while True:
        for chat_id in subscribers:
            try:
                bot.send_message(chat_id, "Это автоматическое сообщение!")
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")
        time.sleep(86400)  # Задержка между отправками (в секундах)

# Запуск бота
if __name__ == '__main__':
    Thread(target=send_periodic_messages).start()
    bot.polling(none_stop=True)

