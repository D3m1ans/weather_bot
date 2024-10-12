import json
import requests
import telebot

bot = telebot.TeleBot('5889143649:AAEZDxqe8vTcd46zxEps4Tp5wqnLaMmjmag')
API = 'b1d12b01e343f1c3941a7e242c6c57c5'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, я бот, который подскажет тебе погоду.'
                                      f'Для этого пропиши команду /weather')

@bot.message_handler(commands=['weather'])
def get_weather(message):
    weat = bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(weat, city_step)

def city_step(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]

        bot.reply_to(message, f'Погода в данный момент: {temp} градуса')
    else:
        bot.send_message(message.chat.id, 'Город указан некорректно')
        bot.register_next_step_handler(message, city_step)

bot.polling(none_stop=True)