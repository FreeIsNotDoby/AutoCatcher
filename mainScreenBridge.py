import os
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
from compare import  CompareImage

# 참고 : https://wikidocs.net/35482
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form_class = uic.loadUiType(BASE_DIR + r'\mainScreen.ui')[0]


class mainScreenBridge(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        image_size = (450, 450)
        interval = 8

        # additional windows
        self.blocker = ScreenBlocker(self.__position_selected)
        self.settingWidget = SettingWidget(self.__setting_changed, image_size, interval)
        self.helpScreen = HelpScreen()

        self.findButton.clicked.connect(self.__find_button_clicked)
        self.setBasePosButton.clicked.connect(self.__set_base_pos_button_clicked)
        self.settingButton.clicked.connect(self.__setting_button_clicked)
        self.helpButton.clicked.connect(self.__help_button_clicked)

        self.compare = CompareImage((0, 0), image_size, interval)

    def __find_button_clicked(self):
        result = self.compare.crop_image_and_compare()
        buffer = QtGui.QPixmap.fromImage(result)
        pixmap = QtGui.QPixmap(buffer)
        self.resultImage.setPixmap(pixmap)
        print("find button click!")

    def __set_base_pos_button_clicked(self):
        self.blocker.show()

    def __position_selected(self, position):
        self.compare.set_base_position((position.x(), position.y()))

    def __setting_button_clicked(self):
        self.settingWidget.show()

    def __setting_changed(self, changed):
        self.compare.set_image_size((changed[0], changed[1]))
        self.compare.set_image_interval(changed[2])

    def __help_button_clicked(self):
        self.helpScreen.show()


class SettingWidget(QWidget):
    def __init__(self, setting_changed_callback, image_size, interval):
        super().__init__()

        self.image_size = image_size
        self.interval = interval

        self.setting_changed_callback = setting_changed_callback
        layout = QFormLayout()

        self.width_label = QLabel('이미지 너비')
        self.width_edit = QLineEdit(str(self.image_size[0]))
        self.width_edit.setValidator(QIntValidator(1, 3000, self))
        layout.addRow(self.width_label, self.width_edit)

        self.height_label = QLabel('이미지 높이')
        self.height_edit = QLineEdit(str(self.image_size[1]))
        self.height_edit.setValidator(QIntValidator(1, 3000, self))
        layout.addRow(self.height_label, self.height_edit)

        self.interval_label = QLabel('이미지 사이 간격')
        self.interval_edit = QLineEdit(str(self.interval))
        self.interval_edit.setValidator(QIntValidator(0, 1000, self))
        layout.addRow(self.interval_label, self.interval_edit)

        self.button = QPushButton("적용")
        self.button.clicked.connect(self.__apply_button_clicked)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def __apply_button_clicked(self):
        changed = (int(self.width_edit.text()), int(self.height_edit.text()), int(self.interval_edit.text()))
        self.setting_changed_callback(changed)
        self.close()


class ScreenBlocker(QWidget):
    def __init__(self, position_select_callback):
        super().__init__()

        screen_rect = QApplication.desktop().screenGeometry()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        background_block = QWidget()
        background_block.setStyleSheet('background-color: rgba(255,255,255,0.5);')

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(background_block)

        self.setLayout(layout)
        self.setGeometry(screen_rect)

        self.position_select_callback = position_select_callback

    def mousePressEvent(self, event):

        print('pos : ' + str(event.pos()))
        self.position_select_callback(event.pos())
        self.close()

class HelpScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        label = QLabel('틀린 그림 찾아 드립니다.\n\n'
                       '사용법\n'
                       '1. 기준점 설정 클릭(화면 전체가 불투명해짐), \n'
                       '   왼쪽 이미지의 좌측 상단 모서리 클릭\n'
                       '2. 찾기! 버튼 클릭\n'
                       '3. 빨갛게 표시된 부분을 찾는다\n\n'
                       '설정\n'
                       '이미지 너비 : 이미지 너비 설정, 기본값 450px\n'
                       '이미지 높이 : 이미지 높이 설정, 기본값 450px\n'
                       '이미지 사이 간격 : 이미지 둘 사이의 간격, 기본값 8px\n')

        layout.addWidget(label)
        self.setLayout(layout)
