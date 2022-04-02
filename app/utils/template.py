import os
from app import config
import telebot.types as t


class Template:
    @classmethod
    def load(cls, name: str, message: t.Message | dict = {}) -> str:
        template_path = os.path.join(
            config.PROJECT_PATH, f'app\\templates\\{name}')
        with open(template_path, encoding='utf8') as f:
            content = ''.join(f.readlines()).format(message=message)
        return content
