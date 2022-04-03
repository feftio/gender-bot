from venv import create
import telebot
import telebot.types as t
from app import config
from app.utils.decorators import init_decorators
from app.db.operations import create_answer, create_respondent, get_question, init_db, get_answer, update_answer
from app.db.tables import Form, Respondent
from app.utils.template import Template
from app.utils.buttons import inline_markup, reply_markup
from app.db.core import Session
from sqlalchemy import select

init_db()
bot = init_decorators(telebot.TeleBot(config.TOKEN, parse_mode='HTML'))
current_form_id = 1


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: t.CallbackQuery):
    if '|' in call.data:
        q, a = call.data.split('|')
        update_answer(call.from_user.id, current_form_id, {q: a})

    answer = get_answer(call.from_user.id, current_form_id)
    for question_index, variant in answer.items():
        if variant is None:
            question, variants = get_question(
                current_form_id, call.from_user.id, question_index)
            _variants = []
            for i in range(len(variants)):
                _variants.append((variants[i], f'{question_index}|{i}'))
            bot.send_message(
                chat_id=call.from_user.id,
                text=question,
                reply_markup=inline_markup(_variants)
            )
            break


@bot.message_handler(commands=['start'])
def start(message: t.Message):
    create_respondent(message)
    create_answer(
        respondent_id=message.from_user.id,
        form_id=current_form_id
    )
    return bot.send_message(
        chat_id=message.chat.id,
        text=Template.load('start.html', message),
        reply_markup=inline_markup([('Начать опрос', 'start_form')])
    )


# Don't touch


@bot.message_handler(commands=['words'])
def words(message: t.Message):
    words = Template.list('words')
    return bot.send_message(
        chat_id=message.chat.id,
        text='- ' + '\n- '.join(words),
        reply_markup=reply_markup(words)
    )

# Don't touch


@bot.message_handler(content_types=['text'])
def word(message: t.Message):
    if message.text in Template.list('words'):
        text = Template.load(f'words/{message.text}.html')
    else:
        text = 'Такого термина нет в нашей базе.'
    return bot.reply_to(
        message=message,
        text=text
    )


bot.infinity_polling()
