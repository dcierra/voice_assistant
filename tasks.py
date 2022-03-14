import pyttsx3
import webbrowser
import os
from PyQt5 import QtWidgets
import pyautogui


class Tasks:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Aleksandr-hq':
                self.engine.setProperty('voice', voice.id)

    def say(self, value):
        self.engine.say(value)
        self.engine.runAndWait()

    def greetings(self):
        try:
            self.say('Приветствую')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def goodbye(self):
        try:
            self.say('Всего доброго')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def search_something(self, value):
        try:
            self.say('Выполняю поиск по вашему запросу')
            webbrowser.get('windows-default').open(f'www.google.com/search?client=opera-gx&q={value}')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def open_lk_nsuem(self):
        try:
            self.say('Открываю личный кабинет НГУЭУ')
            webbrowser.get('windows-default').open('https://lk.nsuem.ru')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def open_rasp_nsuem(self):
        try:
            self.say('Открываю расписание')
            webbrowser.get('windows-default').open('https://rasps.nsuem.ru/group/11-ПИ001')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def shutdown_pc(self):
        try:
            self.say('Выключаю компьютер')
            os.system('shutdown /s /t 1')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def open_my_pc(self):
        try:
            self.say('Открываю Мой Компьютер')
            os.system('explorer file://')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def open_recycle_bin(self):
        try:
            self.say('Открываю корзину')
            os.system('start shell:RecycleBinFolder')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def open_presentation(self):
        try:
            self.say('Выберите путь до презентации')
            self.path = QtWidgets.QFileDialog.getOpenFileName()[0]
            os.startfile(self.path)
        except:
            self.say('Возникла непредвиденная ошибка.')

    def presentation_full_screen(self):
        try:
            self.say('Открываю презентацию на полный экран')
            pyautogui.press('f5')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def next_slide(self):
        try:
            self.say('Переключаю на следующий слайд')
            pyautogui.press('N')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def last_slide(self):
        try:
            self.say('Переключаю на предыдущий слайд')
            pyautogui.press('P')
        except:
            self.say('Возникла непредвиденная ошибка.')

    def exit_presentation(self):
        try:
            self.say('Выхожу из презентации')
            pyautogui.hotkey('esc')
        except:
            self.say('Возникла непредвиденная ошибка.')
