from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('startscreen.ui', self)
        img = QPixmap('resource/main_window.jpg')
        self.image.setPixmap(img.scaled(1091, 801))
        self.btngrp.buttonClicked.connect(self.mov)
        self.play.clicked.connect(self.startplay)
        self.diff = 'легкий уровень'

    def mov(self, button):
        self.diff = button.text()

    def startplay(self):
        import Танчики
        self.hide()
        Танчики.main(self.diff)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = StartWindow()
    a.show()
    sys.exit(app.exec())