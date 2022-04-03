import os
from app import config
import telebot.types as t


class Template:
    @classmethod
    def load(cls, path: str, message: t.Message | dict = {}) -> str:
        template_path = os.path.join(
            config.PROJECT_PATH, f'app\\templates\\{path}'
        )
        with open(template_path, encoding='utf8') as f:
            content = ''.join(f.readlines()).format(message=message)
        return content

    @classmethod
    def list(cls, path: str):
        folder_path = os.path.join(
            config.PROJECT_PATH, f'app\\templates\\{path}'
        )
        return list(map(lambda filename: filename.split('.')[0], os.listdir(folder_path)))


if __name__ == '__main__':
    print(Template.list('words'))
