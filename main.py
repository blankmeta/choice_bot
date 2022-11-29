import logging
import os

import telebot
from dotenv import load_dotenv
from telebot import types

from choice_logic import Asker
from config import sticker_id

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s, %(levelname)s, '
                                       '%(message)s, '
                                       '%(name)s, %(funcName)s, '
                                       '%(lineno)s'))
logger.addHandler(handler)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

# class User:
#     def __init__(self):

userid_to_queue = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_sticker(message.chat.id, sticker_id['hello'])
    msg = bot.send_message(message.chat.id,
                           f'Привет! Напиши варианты через запятую',
                           reply_markup=markup,
                           parse_mode='markdown')
    bot.register_next_step_handler(msg, init)


def init(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2,
                                       resize_keyboard=True)

    choices = message.text.split(',')
    choices = list(map(str.strip, choices))  # Remove leading whitespaces
    choices = list(set(choices))  # Remove repeats and shuffle choices
    a = Asker(choices)
    userid_to_queue[message.from_user.id] = a
    first_variant, second_variant = a.ask()
    markup.add(first_variant, second_variant)
    msg = bot.send_message(message.chat.id,
                           f'{first_variant} or {second_variant}',
                           parse_mode='markdown', reply_markup=markup)
    bot.register_next_step_handler(msg, next_step)


def next_step(message):
    a = userid_to_queue[message.from_user.id]
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2,
                                           resize_keyboard=True)
        a.answer(message.text)
        first_variant, second_variant = a.ask()
        markup.add(first_variant, second_variant)
        msg = bot.send_message(message.chat.id,
                               f'{first_variant} or {second_variant}',
                               parse_mode='markdown', reply_markup=markup)
        bot.register_next_step_handler(msg, next_step)
    except IndexError as e:
        markup = types.ReplyKeyboardRemove(selective=False)
        result = '\n'.join(a.rating[::-1])
        msg = bot.send_message(message.chat.id,
                               result,
                               parse_mode='markdown', reply_markup=markup)
        bot.register_next_step_handler(msg, send_welcome)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()

if __name__ == '__main__':
    pass
