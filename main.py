import dotenv
from telebot import TeleBot, types, formatting

from parser import parse

api_token = dotenv.get_key('.env', 'TOKEN')

bot = TeleBot(token=api_token)

parse_mode = 'HTML'

func_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
func_keyboard.add('Поиск кинокартины🎬🔍')
func_keyboard.add('Поиск песни/исполнителя🎵🔍')
func_keyboard.add('Сообщить об ошибке❗️')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     formatting.hbold(
                         'Привет, это бот по поиску аналогов ваших любимых фильмов/сериалов/песен и исполнителей'),
                     parse_mode)
    bot.send_message(message.chat.id, formatting.hbold('Выберите фунцию'), parse_mode, reply_markup=func_keyboard)


@bot.message_handler(func=lambda message: True)
def recognize_func(message):
    if message.text:
        if message.text == 'Поиск кинокартины🎬🔍':
            key = 'f'
            bot.send_message(message.chat.id, formatting.hbold('Напишите название кинокартины'), parse_mode)
            bot.register_next_step_handler(message, search_film, key)
        if message.text == 'Поиск песни/исполнителя🎵🔍':
            key = 'm'
            bot.send_message(message.chat.id, formatting.hbold(
                'Напишите название песни/исполнителя\n🛑Названия на русском не всегда работают коректно'), parse_mode)
            bot.register_next_step_handler(message, search_film, key)
        if message.text == 'Сообщить об ошибке❗️':
            bot.send_message(message.chat.id, formatting.hbold('Опишите вашу проблему'), parse_mode)
            bot.register_next_step_handler(message, error_debug)


def search_film(film_title, key):
    film_list = parse(film_title.text, key)
    if key == 'f':
        media_type = 'кинокартин'
    if key == 'm':
        media_type = 'песен/исполнителей'

    if len(film_list) > 0:
        bot.send_message(film_title.chat.id,
                         formatting.hbold(f'Найдено {len(film_list)} {media_type}✅\n') + formatting.hitalic(
                             '\n'.join(film_list)), parse_mode)
    else:
        bot.send_message(film_title.chat.id,
                         formatting.hbold('Похоже ничего не найдено'), parse_mode)


def error_debug(message):
    id_owner = 564600205
    bot.send_message(message.chat.id, formatting.hbold('Благодарим за ваш ответ❤️'), parse_mode)
    bot.send_message(id_owner, formatting.hbold(f'Поступила проблема\n') + message.text + message.chat.id, parse_mode)


if __name__ == '__main__':
    bot.infinity_polling()
