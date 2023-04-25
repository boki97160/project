from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cv2


class Input_keys:
    def __init__(self):
        pass
    def initUI(self,app):
        self.app = app
        self.screen = QApplication.desktop()
        self.form = QWidget()
        # TODO: form size
        
        self.form.resize(1000,800)
        self.input_abbr()
        self.form.show()

    def input_abbr(self):
        pass