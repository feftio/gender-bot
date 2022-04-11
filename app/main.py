import telebot
import telebot.types as t
from app import config
from app.forms import form as form_body
from app.db.core import engine, Base
from app.utils.decorators import init_decorators
from app.db.tables import Respondent, Answer, Form
from app.utils.buttons import inline_markup, reply_markup
from app.utils.template import Template


""" Database init """
Base.metadata.create_all(engine, checkfirst=True)
Form.create(name='Form Name', body=form_body)


""" Bot init """
bot = init_decorators(telebot.TeleBot(config.TOKEN, parse_mode='HTML'))
current_form_id = Form.get_by_name('Form Name').id


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: t.CallbackQuery):
    if '|' in call.data:
        q, a = call.data.split('|')
        Answer.update(call.from_user.id, current_form_id, {q: a})

    answer_body = Answer.get(
        respondent_id=call.from_user.id,
        form_id=current_form_id
    ).body
    for question_index, variant_index in answer_body.items():
        if variant_index is None:
            question, variants = Form.get_question(
                form_id=current_form_id,
                question_index=question_index
            )
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
    Respondent.create(
        respondent_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    Answer.create_empty(
        respondent_id=message.from_user.id,
        form_id=current_form_id
    )
    return bot.send_message(
        chat_id=message.chat.id,
        text=Template.load('start.html', message),
        reply_markup=inline_markup([('Начать опрос', 'start_form')])
    )


@bot.message_handler(commands=['words'])
def words(message: t.Message):
    words = Template.list('words')
    return bot.send_message(
        chat_id=message.chat.id,
        text='🧩 ' + '\n🧩 '.join(words),
        reply_markup=reply_markup(words)
    )


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
