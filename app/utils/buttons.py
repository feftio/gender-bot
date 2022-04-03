import telebot.types as t


def reply_markup(labels: list, row_width: int = 3):
    markup = t.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for label in labels:
        markup.add(label)
    return markup


def inline_markup(data: list, row_width: int = 3):
    markup = t.InlineKeyboardMarkup(row_width=row_width)
    for label, callback in data:
        markup.add(t.InlineKeyboardButton(label, callback_data=callback))
    return markup
