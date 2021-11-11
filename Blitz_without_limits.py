import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from KeyBoardLayout import Ui_MainWindow
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint
from PyQt5.QtMultimedia import QSound
from time import sleep
from random import choice, shuffle
import datetime as dt


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Key_Return.clicked.connect(self.change_button_color)
        self.Key_Return.animateClick(0.01)

        self.window_width = int(str(self.geometry())[24:29])
        self.window_high = int(str(self.geometry())[31:35])
        self.verticalLayoutWidget.setGeometry(QRect((self.window_width - 1481) // 2, 540, 1481, 556))
        self.parametrs.move((self.window_width - 1231) // 2, 101)
        self.words.move((self.window_width - 1741) // 2, 320)
        self.x_of_cursor = (self.window_width - 1741) // 2 - 2
        self.cursor_.setGeometry(self.x_of_cursor, 310, 21, 60)

        for button in self.buttonGroup.buttons():
            button.clicked.connect(self.tap_on_symbol_button)
        self.Key_BracketLeft.setText('{\n[')
        self.Key_BracketRight.setText('}\n]')
        self.Key_Backslash.setText('|\n\\')
        self.Key_Semicolon.setText(':\n;')
        self.Key_Apostrophe.setText('''"\n\'''')
        self.Key_Slash.setText('?\n/')

        self.Key_Return.clicked.connect(self.tap_on_enter)
        self.Key_Backspace.clicked.connect(self.tap_on_backspace)
        self.right_shift.clicked.connect(self.tap_on_shift)

        self.noise = QSound('broken_window.wav')
        self.start_time = 0
        self.mistakes = 0
        self.curpos = 0
        self.diary = {}
        self.len_words = 0
        self.PRINT_BUTTONS = list(map(lambda x: x.text()[-1], self.buttonGroup.buttons()))
        self.PRINT_BUTTONS_SHIFT = list(map(lambda x: x.text()[0], self.buttonGroup.buttons()))
        with open('key_words.txt', 'r') as words:
            for i in range(2, 9):
                self.diary[i] = list(map(lambda x: x.lower(), words.readline()[:-1].split(', ')))
        self.text_generator()

        self.widget.resize(200, self.window_high)
        self.widget.move(self.window_width, 0)
        self.animate = QPropertyAnimation(self.widget, b"pos")
        self.animate.setEndValue(QPoint(300, 300))
        self.animate.setDuration(400)


    def change_button_color(self):
        self.setStyleSheet("QPushButton {background-color: rgb(51,122,183); "
                           "color: White; border-radius: 8} "
                           "QPushButton:pressed {background-color:rgb(34, 255, 17) ; }")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.Key_Backspace.animateClick(40)

        if e.key() == Qt.Key_Return:
            self.Key_Return.animateClick(40)

        if e.key() in map(lambda x: ord(x), self.PRINT_BUTTONS):
            self.click_button(e, self.tap_on_symbol_button, self.PRINT_BUTTONS)

        if int(e.modifiers()) == Qt.ShiftModifier:
            if e.key() in map(lambda x: ord(x), self.PRINT_BUTTONS):
                self.click_button(e, self.tap_on_symbol_button_shift, self.PRINT_BUTTONS_SHIFT)

    def restore(self):
        self.text_generator()
        self.mistakes = 0
        self.accuracy.setText('Accuracy: 0')
        self.misses.setText(f'Mistakes: {self.mistakes}')
        self.speed.setText('Speed: 0')
        self.start_time = 0

    def block_buttons(self):
        for button in self.buttonGroup.buttons():
            button.setDisabled(True)
        self.Key_Return.setEnabled(True)
        self.Key_Return.setStyleSheet("background-color: rgb(34, 255, 17); color: White; border-radius: 8")

    def text_generator(self):
        text = []
        volume = 0
        while volume < 86:
            group = choice([2, 3, 4, 5, 6, 7, 8])
            text.append(choice(self.diary[group]))
            volume += group + 1
        while volume + 4 < 96:
            text.append(choice(self.diary[3]))
            volume += 4
        else:
            if volume + 2 < 96:
                text.append(choice(self.diary[2]))
        shuffle(text)
        self.len_words = len(' '.join(text))
        self.words.setText(' '.join(text))

    def tap_on_symbol_button(self):
        if self.speed.text() == 'Speed: 0':
            self.start_time = dt.datetime.now()
        if self.curpos == self.len_words - 1:
            self.block_buttons()
            return
        if self.words.text()[self.curpos] != self.sender().text()[-1].lower():
            self.noise.play()
            self.mistakes += 1
            self.misses.setText(f'Mistakes: {self.mistakes}')
        self.speed.setText(f'Speed: {int(self.curpos / ((dt.datetime.now() - self.start_time).total_seconds() / 60))}')
        if self.mistakes == 0:
            self.accuracy.setText('Accuracy: 100')
        else:
            self.accuracy.setText(f'Accuracy: {int((self.curpos - self.mistakes + 1) /(self.curpos + 1) * 100)}')
        self.curpos += 1
        self.cursor_.setGeometry(self.x_of_cursor + 18 * self.curpos + 1, 310, 21, 60)
        self.animate.setEndValue(QPoint(self.window_width - 200, 0))
        self.animate.setDuration(2000)
        self.animate.start()

    def tap_on_symbol_button_shift(self):
        if self.speed.text() == 'Speed: 0':
            self.start_time = dt.datetime.now()
        if self.curpos == self.len_words - 1:
            self.block_buttons()
            return
        if self.words.text()[self.curpos] != self.sender().text()[0]:
            self.noise.play()
            self.mistakes += 1
            self.misses.setText(f'Mistakes: {self.mistakes}')
        self.speed.setText(f'Speed: {int(self.curpos / ((dt.datetime.now() - self.start_time).total_seconds() / 60))}')
        if self.mistakes == 0:
            self.accuracy.setText('Accuracy: 100')
        else:
            self.accuracy.setText(f'Accuracy: {int((self.curpos - self.mistakes + 1) /(self.curpos + 1) * 100)}')
        self.curpos += 1
        self.cursor_.setGeometry(self.x_of_cursor + 18 * self.curpos + 1, 310, 21, 60)

    def tap_on_backspace(self):
        if self.curpos == 0:
            return
        elif self.curpos == self.len_words - 1:
            return
        self.curpos -= 1
        self.cursor_.setGeometry(self.x_of_cursor + 18 * self.curpos, 310, 21, 60)

    def tap_on_enter(self):
        for button in self.buttonGroup.buttons():
            button.setDisabled(False)
        self.cursor_.setGeometry(self.x_of_cursor, 310, 21, 60)
        self.curpos = 0
        self.Key_Return.setStyleSheet("QPushButton {background-color: rgb(51,122,183); color: White; "
                                 "border-radius: 8;} "
                                 "QPushButton:pressed {background-color:rgb(34, 255, 17) ; }")
        self.restore()

    def tap_on_shift(self):
        pass

    def click_button(self, event, to_connect, to_find):
        button = self.buttonGroup.buttons()[self.PRINT_BUTTONS_SHIFT.index(f'{chr(event.key())}')]
        button.disconnect()
        button.clicked.connect(to_connect)
        button.animateClick(40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.showFullScreen()
    sys.exit(app.exec())


