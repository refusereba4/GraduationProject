from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QMainWindow,
                             QGridLayout, QApplication, QPushButton, QLabel, QLineEdit)

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
# from predictsingle import predict
from PIL import Image
import predictclass


class Ui_example(QWidget):
    def __init__(self):
        super().__init__()  # 主函数了

        self.layout = QGridLayout(self)  # 创建一个整体界面
        self.setStyleSheet('background:green')
        self.label_image = QLabel(self)  # 选择图片后显示图片的标签
        self.label_predict_result = QLabel('识别结果', self)  # 识别结果文本提示标签
        self.label_predict_result_display = QLabel(self)  # 识别结果标签
        self.label_predict_acc = QLabel('识别准确率', self)  # 识别准确率文本提示标签
        self.label_predict_acc_display = QLabel(self)  # 识别准确率结果标签

        self.button_search_image = QPushButton('选择图片', self)  # 选择图片的文本提示标签
        self.button_run = QPushButton('运行', self)  # 运行标签
        self.setLayout(self.layout)  # 设置程序界面,并将创建的界面添加到这里
        self.initUi()  # 调用下面的方法,将初始化函数中的这个self传进去

    def initUi(self):
        self.layout.addWidget(self.label_image, 1, 1, 3, 2)  # 将上面创建的一系列标签按追加到界面中,并设置显示位置
        self.layout.addWidget(self.button_search_image, 1, 3, 1, 2)
        self.layout.addWidget(self.button_run, 3, 3, 1, 2)
        self.layout.addWidget(self.label_predict_result, 4, 3, 1, 1)
        self.layout.addWidget(self.label_predict_result_display, 4, 4, 1, 1)
        self.layout.addWidget(self.label_predict_acc, 5, 3, 1, 1)
        self.layout.addWidget(self.label_predict_acc_display, 5, 4, 1, 1)

        self.button_search_image.clicked.connect(self.openimage)  # 对选择图片按钮设置点击操作,点击后执行openimage操作
        self.button_run.clicked.connect(self.run)  # 对运行按钮执行运行函数 self.openimage self.run指的应该是本类函数

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('flowers-10十分类')
        self.show()

    def openimage(self):
        global fname
        imgName, imgType = QFileDialog.getOpenFileName(self, "选择图片", "", "*.jpg;;*.png")  # imgName返回文件绝对路径
        # imgType返回文件类型即拓展名
        print('imgName:{}'.format(imgName))
        print('imgType:{}'.format(imgType))
        jpg = QPixmap(imgName).scaled(self.label_image.width(), self.label_image.height())
        self.label_image.setPixmap(jpg)
        fname = imgName

    def run(self):
        global fname
        print('type(fname):{}'.format(type(fname)))
        # file_name = str(fname) #下面去掉了对fname的强转str的操作，因为上面打印fname类型发现已经是str了
        file_name = fname
        img = Image.open(file_name)

        a, b = predictclass.predict(img)
        self.label_predict_result_display.setText(a)
        self.label_predict_acc_display.setText(str(b))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_example()
    sys.exit(app.exec_())
