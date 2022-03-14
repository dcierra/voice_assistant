import sys
from assistant_ui import *
from thread_methods import *
from tasks import *
from PyQt5 import QtWidgets
import speech_recognition as sr


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создание словаря с командами
        self.commands = {
            'greetings': ['привет', 'приветствую', 'здравствуйте'],
            'goodbye': ['пока', 'прощай', 'до свидания'],
            'open_lk_nsuem': ['открой личный кабинет', 'личный кабинет'],
            'open_rasp_nsuem': ['открой расписание', 'расписание'],
            'shutdown_pc': ['выключи компьютер'],
            'open_my_pc': ['открой мой компьютер'],
            'open_recycle_bin': ['открой корзину'],
            'open_presentation': ['открой презентацию', 'открыть презентацию'],
            'presentation_full_screen': ['презентация на полный экран', 'открой презентацию на полный экран'],
            'next_slide': ['следующий слайд'],
            'last_slide': ['предыдущий слайд'],
            'exit_presentation': ['закрой презентацию', 'выйди из презентации']
        }

        # Убираем рамки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.user_can_drag_window()

        # Обработчики кнопок
        self.ui.tBtn_minimaze.clicked.connect(self.minimize_window)
        self.ui.tBtn_closeWindow.clicked.connect(self.close_window)
        self.ui.tBtn_start_speaking.clicked.connect(self.start_speaking)
        self.ui.tBtn_check_micro.clicked.connect(self.check_microphone)
        self.ui.tBtn_commands.clicked.connect(self.show_commands)

        # Создание потока
        self.thread_handler = ThreadRecord()
        self.thread_handler.signal.connect(self.signal_handler)

        # Создание задач
        self.tasks = Tasks()

    # Методы позволяющие пользователю двигать окно
    def user_can_drag_window(self):
        fg = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # Методы кнопок
    def close_window(self):
        if QtWidgets.QMessageBox.warning(self, 'Выход', 'Вы действительно хотите выйти?',
                                         QtWidgets.QMessageBox.Yes,
                                         QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            raise SystemExit
        else:
            return

    def minimize_window(self):
        self.showNormal()
        self.showMinimized()

    def start_speaking(self):
        if self.ui.tBtn_start_speaking.text().lower() == 'начать':
            self.signal_handler(['start'])
            self.thread_handler.handler_status = True
            self.thread_handler.start()
        else:
            self.signal_handler(['stop'])
            self.thread_handler.handler_status = False

    def check_microphone(self):
        microphone_list = sr.Microphone.list_microphone_names()
        if len(microphone_list) > 0:
            QtWidgets.QMessageBox.about(self, 'Микрофоны в системе', str(microphone_list))
        else:
            QtWidgets.QMessageBox.about(self, 'Микрофоны в системе', 'Микрофонов не найдено')

    def show_commands(self):
        QtWidgets.QMessageBox.about(self, 'Доступные команды', '1) Приветствие (привет, приветствую, здравствуйте)\n'
                                                               '2) Попрощаться (пока, прощай, до свидания)\n'
                                                               '3) Открыть личный кабинет (открой личный кабинет,'
                                                               ' личный кабинет)\n'
                                                               '4) Открыть расписание (открой расписание, расписание)\n'
                                                               '5) Поиск в гугл (поиск.. или найди..)\n'
                                                               '6) Выключить компьютер (выключи компьютер)\n'
                                                               '7) Открыть мой компьютер (открой мой компьютер)\n'
                                                               '8) Открыть корзину (открой корзину)\n'
                                                               '9) Открыть презентацию (открой презентацию,'
                                                               ' открыть презентацию)\n'
                                                               '10) Открыть презентацию на полный экран (презентация '
                                                               'на полный экран, открой презентацию на полный экран)\n'
                                                               '11) Следующий слайд (следующий слайд)\n'
                                                               '12) Предыдущий слайд (предыдущий слайд)\n'
                                                               '13) Закрыть презентацию (закрой презентацию, '
                                                               'выйди из презентации)')

    # Обработчик сигналов
    def signal_handler(self, value: list):
        if value[0] == 'start':
            self.ui.output_text_information.clear()
            self.ui.output_text_information.appendPlainText('Ассистент запущен, говорите')
            self.ui.tBtn_start_speaking.setText('Закончить')

        elif value[0] == 'response':
            ans = value[1].split(': ')[1]
            self.ui.output_text_information.appendPlainText(value[1])

            for key, value in self.commands.items():
                if ans in value:
                    call_func = f'self.tasks.{key}()'
                    eval(call_func)

                    if key == 'goodbye':
                        self.signal_handler(['stop'])
                        self.thread_handler.handler_status = False
                elif ans.split()[0] == 'найди' or ans.split()[0] == 'поиск':
                    self.tasks.search_something(ans.replace(ans.split()[0], ''))
                    break


        elif value[0] == 'stop':
            self.ui.output_text_information.appendPlainText('Всего доброго')
            self.ui.tBtn_start_speaking.setText('Начать')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    assistant = GUI()
    assistant.show()
    sys.exit(app.exec_())
