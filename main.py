import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
from telebot import types
bot = telebot.TeleBot("5685529037:AAEl81HPKnjO56sRiK6ZUqd5keHnNe_dyBU")

@bot.message_handler(commands=["start"])
def start (message):
    #Клавиатура с кнопкой запроса локации
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)

 #Получаю локацию
@bot.message_handler(content_types=['location'])
def location (message):
    if message.location is not None:
        print(message.location)
        print(message)

def get_address_from_coords(location):
    PARAMS = {
        "apikey": "f073aa96-50da-464d-b192-23954c938854",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": location
    }
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\n\nОтправь мне локацию или координаты (долгота, широта):"

#Эта функция будет использоваться, если пользователь послал локацию.
def location(update, context):
    #получаем обьект сообщения (локации)
    message = update.message
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)
    
def main():
    #создаем бота и указываем его токен
    updater = Updater("5685529037:AAEl81HPKnjO56sRiK6ZUqd5keHnNe_dyBU", use_context=True)
    #создаем регистратор событий, который будет понимать, что сделал пользователь и на какую функцию надо переключиться.
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.location, location))
    #запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #запускаем функцию def main
    main()

bot.polling(none_stop = True)
input()
