import pyttsx3
import webbrowser


class Tasks:
    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self, value):
        self.engine.say(value)
        self.engine.runAndWait()

    def greetings(self):
        self.say('Приветствую')

    def goodbye(self):
        self.say('Всего доброго')

    def search_something(self, value):
        self.say('Выполняю поиск по вашему запросу')
        webbrowser.get('windows-default').open(f'www.google.com/search?client=opera-gx&q={value}')

    def open_lk_nsuem(self):
        self.say('Открываю личный кабинет НГУЭУ')
        webbrowser.get('windows-default').open('https://lk.nsuem.ru')

    def open_rasp_nsuem(self):
        self.say('Открываю расписание')
        webbrowser.get('windows-default').open('https://rasps.nsuem.ru/group/11-ПИ001')
