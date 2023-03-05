# coding=utf-8
import sys

import cv2
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout, QSlider, QFileDialog,
                             QMessageBox)
import numpy as np
from yolo import YOLO

yolo = YOLO()
capture = cv2.VideoCapture(1)
fps = 0.0


class SanUI3(QWidget):
    """基础Gui页面"""

    # 使用说明界面，加一些使用说明的文字就可以了，没什么大用

    def __init__(self):
        super().__init__()
        self.init_ui()  # 主窗口

    def init_ui(self):
        # self.setGeometry(300, 300, 600, 200)  # 设置主窗口的位置和大小
        self.layout = QGridLayout()

        self.setStyleSheet(
            # 'QLabel{font-size:18px;color:rgb(248,181,0)}'
            'QLabel{font-size:18px;margin-left:10px}'
            'QPushButton{font-size:12px;background:rgb(255,223,140);}'
            'QMessageBox{color:black;font-size:10px}'

            # 'QGridLayout{margin-top:-20px}'
        )
        # self.QMessageBox.setStyleSheet('')

        # self.label_uselabel = QLabel('使用说明:')
        # self.label_singleimg.setStyleSheet(
        #     '{margin-top:-20px}'
        # )
        # self.label_instruction = QLabel('一共有两个功能模块，即水果图片分类与水果图片标注')
        self.label_fenlei = QLabel('水果实时标注:')
        self.label_fenlei.setStyleSheet('margin-left:0px')
        self.btn_cameractrl = QPushButton('开启检测')
        # self.btn_close = QPushButton('关闭检测')

        # self.framelabel = QLabel()
        self.label = QLabel()
        self.label.setFixedSize(720, 576)
        self.label.setPixmap(QPixmap('camera.png').scaled(720, 576))
        self.label.setStyleSheet('border:5px solid gray;border-radius:15px')

        # self.layout.addWidget(self.label_fenlei, 0, 1, 1, 1)
        self.layout.addWidget(self.btn_cameractrl, 1, 1, 1, 1)
        self.layout.addWidget(self.label, 0, 2, 3, 3)
        # self.layout.addWidget(self.btn_close, 2, 1, 1, 1)

        self.btn_cameractrl.clicked.connect(lambda: self.run())
        # self.btn_close.clicked.connect(lambda: self.closeVideo())
        # self.btn_cameractrl.clicked.connect(lambda: self.run())
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)

        self.setLayout(self.layout)

    def run(self):

        if self.btn_cameractrl.text() == '开启检测':
            self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
            self.timer.timeout.connect(self.capPicture)
            self.label.setStyleSheet('border:none')
            self.btn_cameractrl.setText('关闭检测')
        else:
            print('关闭摄像头')
            self.btn_cameractrl.setText('开启检测')
            self.label.setPixmap(QPixmap('camera.png').scaled(720, 576))
            self.label.setStyleSheet('border:5px solid gray;border-radius:15px')
            self.cap.release()

    def capPicture(self):
        if (self.cap.isOpened()):
            # get a frame
            ret, img = self.cap.read()
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(img))
            # 进行检测
            img = np.array(yolo.detect_imagevideo(frame))
            # 变换彩色空间顺序
            # cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            # 转为QImage对象
            self.image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.image).scaled(self.label.width(), self.label.height()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = SanUI3()
    sys.exit(app.exec_())
