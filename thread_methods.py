import speech_recognition as sr
from PyQt5 import QtCore


class ThreadRecord(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    handler_status = True

    def run(self):
        self.signal.emit(['start'])
        while True:
            try:
                if self.handler_status:
                    self.record = sr.Recognizer()
                    with sr.Microphone() as source:
                        audio = self.record.listen(source)
                        try:
                            task = self.record.recognize_google(audio, language='ru-RU').lower()
                            response = 'Вы сказали: ' + task
                            self.signal.emit(['response', response])
                        except Exception:
                            continue
                else:
                    break
            except Exception:
                self.signal.emit(['response', 'Возникла ошибка'])
                self.signal.emit(['stop'])
                break
