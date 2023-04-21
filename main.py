import telebot
from config import TOKEN
from extensions import keys, Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую Вас в валютном конвертере!\nЧтобы узнать как мной пользоваться,\t'
                                      'выполните комманду /help')

@bot.message_handler(commands=['help'])
def help_(message):
    bot.send_message(message.chat.id, 'Введите:\n1) Валюту, которую хотите перевести\n2) Валюту, в которую хотите '
                                      'перевести\n3) Сумму\n\nВ формате: <первая валюта> <вторая валюта> <сумма>\n'
                                      'Например: доллар рубль 100\n'
                                      'Чтобы посмотреть список валют, дайте команду /values')

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n- '.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message):
    try:
        Converter.get_price(message)
    except APIException as e:
        bot.reply_to(message, f'Произошла ошибка.\n{e}')
    else:
        text = Converter.get_price(message)
        bot.send_message(message.chat.id, text)

bot.infinity_polling()
