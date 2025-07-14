import telebot
from config import TOKEN, CURRENCIES
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_help(message: telebot.types.Message):
    text = (
        "Добро пожаловать в бот-конвертер валют!\n"
        "Чтобы узнать цену валюты, отправьте команду в формате:\n"
        "<имя валюты> <в какую перевести> <количество>\n"
        "Пример: доллар рубль 100\n\n"
        "Увидеть список всех доступных валют: /values"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    text += "\n".join([f"- {key.title()}" for key in CURRENCIES.keys()])
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parts = message.text.strip().split()

        if len(parts) != 3:
            raise APIException("Неверный формат запроса. Ожидается 3 параметра.")

        base, quote, amount = parts
        total = CryptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: {e}")
    except Exception as e:
        bot.reply_to(message, f"Системная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, f"{amount} {base} = {total} {quote}")


bot.polling(non_stop=True)