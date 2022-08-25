import telebot
from extensions import CryptoConverter, ConvertionException
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = """Чтобы начать работу, введите команду боту в следующем формате:\n<има валюты> 
<количество переводимой валюты> 
<в какую валюту переводить.>\nУвидеть список всех доступных валют: /values"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionException("Необходимо ввести 3 параметра.")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, amount, base)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'В {base} {amount} - {total_base} {quote}'
        bot.reply_to(message, text)

bot.polling()
