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

userid_to_queue = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_sticker(message.chat.id, sticker_id['hello'])
    msg = bot.send_message(
        message.chat.id,
        f'Привет! Напиши варианты через запятую',
        reply_markup=markup, parse_mode='markdown'
    )
    bot.register_next_step_handler(msg, init)


@bot.message_handler()
def init(message):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, row_width=2, resize_keyboard=True
    )
    choices = message.text.split(',')
    choices = list(map(str.strip, choices))  # Remove leading whitespaces
    choices = list(set(choices))  # Remove repeats and shuffle choices
    a = Asker(choices)
    userid_to_queue[message.from_user.id] = a
    try:
        first_variant, second_variant = a.ask()
    except ValueError:
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(
            message.chat.id, f'Не понимаю тебя. Напиши варианты через запятую',
            parse_mode='markdown', reply_markup=markup
        )
        bot.register_next_step_handler(msg, init)
    else:
        markup.add(first_variant, second_variant)
        msg = bot.send_message(
            message.chat.id, f'{first_variant} or {second_variant}',
            parse_mode='markdown', reply_markup=markup
        )
        bot.register_next_step_handler(msg, next_step)


def next_step(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    try:
        a: Asker = userid_to_queue[message.from_user.id]
    except KeyError:
        msg = bot.send_message(
            message.chat.id, 'Error, try again',
            parse_mode='markdown', reply_markup=markup
        )
        bot.register_next_step_handler(msg, init)
    else:
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, row_width=2, resize_keyboard=True
        )
        a.answer(message.text)
        if not a.is_ended():
            first_variant, second_variant = a.ask()
            markup.add(first_variant, second_variant)
            msg = bot.send_message(
                message.chat.id,
                f'{first_variant} or {second_variant}',
                parse_mode='markdown', reply_markup=markup
            )
            bot.register_next_step_handler(msg, next_step)
        else:
            bot.send_sticker(message.chat.id, sticker_id['victory'])
            rating = a.ask()
            result = []
            for i, value in enumerate(rating):
                result.append([abs(len(rating) - i), value])
            result[-3][0] = '🥉'
            result[-2][0] = '🥈'
            result[-1][0] = '🥇'

            final_result = 'And the score is:\n'
            for value in result:
                final_result += f'\n{value[0]} — {value[1]}'
            markup.add('Again!')
            msg = bot.send_message(
                message.chat.id, final_result,
                parse_mode='markdown', reply_markup=markup
            )
            bot.register_next_step_handler(msg, send_welcome)


if __name__ == '__main__':
    print('start')
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()
