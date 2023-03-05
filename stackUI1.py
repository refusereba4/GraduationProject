# coding=utf-8
import glob
import os
import shutil
import sys

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout, QSlider, QFileDialog,
                             QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import predictclass


class SanUI1(QWidget):
    """基础Gui页面"""

    def __init__(self):
        super().__init__()
        self.init_ui()  # 主窗口

    def init_ui(self):
        # self.setGeometry(300, 300, 600, 200)  # 设置主窗口的位置和大小
        self.layout = QGridLayout()

        self.setStyleSheet(
            # 'QLabel{font-size:18px;color:rgb(248,181,0)}'
            'QLabel{font-size:18px;}'
            'QPushButton{font-size:12px;background:rgb(255,223,140);}'
            'QMessageBox{color:black;font-size:10px}'

            # 'QGridLayout{margin-top:-20px}'
        )
        # self.QMessageBox.setStyleSheet('')

        self.label_singleimg = QLabel('单图模式:')
        # self.label_singleimg.setStyleSheet(
        #     '{margin-top:-20px}'
        # )
        self.label_image = QLabel()  # 选择图片后显示图片的标签
        # self.label_image.setStyleSheet('{margin-top:-60px}')
        # self.label_image.setStyleSheet('{margin-top:60px}')
        # self.label_image.setStyleSheet('margin-top:-30px')
        self.label_predict_result = QLabel('识别结果:')  # 识别结果文本提示标签
        self.label_predict_result_display = QLabel()  # 识别结果标签
        self.label_predict_acc = QLabel('识别准确率:')  # 识别准确率文本提示标签
        self.label_predict_acc_display = QLabel()  # 识别准确率结果标签

        self.button_search_image = QPushButton('选择图片')  # 选择图片的文本提示标签
        self.button_run = QPushButton('运行')  # 运行标签
        # self.button_run.setStyleSheet('{margin-top:-30px}')
        # self.button_cover = QPushButton()
        # # button_cover.setFlat(True)
        # self.button_cover.setEnabled(False)

        self.label_multiimg = QLabel('多图模式: ')
        self.button_search_dir = QPushButton('选择文件夹')
        self.button_save_dir = QPushButton('保存结果文件夹')
        self.button_dir_display = QPushButton()
        # self.button_dir_display.setStyleSheet('background:white')
        self.button_dir_display.setEnabled(False)
        self.button_dir_display.setStyleSheet('color:black;background:rgb(245,147,33);font-size:20px')
        self.button_savedir_display = QPushButton()
        self.button_savedir_display.setStyleSheet('color:black;background:rgb(245,147,33);font-size:20px')
        self.button_savedir_display.setEnabled(False)
        # self.button_savedir_display.setStyleSheet('color:black')
        self.ratetext = QLabel('识别准确率下限:  ')
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setStyleSheet(

            # 'QSlider::groove:horizontal{height:10px;background:gray;border-radius:5px}'
            # 'QSlider::handle:horizontal{width:20px;height:20px;border-radius:10px;'
            # 'margin:-12px 0px -12px 0px;background:rgb(234,89,62);} '
            # 'QSlider::handle:horizontal{width:20px;height:20px;border-radius:10px;'
            # 'margin:-11px 0px -11px 0px;background:rgb(234,89,62);} '
            # 'QSlider::handle:horizontal{background:rgb(255,223,140)}'

            # 'QSlider::sub-page:horizontal{background:rgb(255,223,140);border-radius:5px}'
            # groove 整体 handle 滑块 add-page 未滑过区域 sub-page 已滑过区域
            'QSlider::handle:horizontal{width:20px;background-color:rgb(255,255,255);margin:-9px 0px -9px '
            '0px;border-radius:10px;}' 
            "QSlider::groove:horizontal{height:5px;background-color:rgb(219,219,219);}"
            "QSlider::add-page:horizontal{background-color:rgb(219,219,219);}"
            "QSlider::sub-page:horizontal{background-color:rgb(26,217,110);}"
        )
        self.rate_slider.setRange(50, 90)
        self.rate_slider.setValue(85)
        self.rate_slider.setSingleStep(5)
        self.ratetext_display = QLabel('85')
        self.ratetext_display.setStyleSheet('padding-left:10px')

        self.button_multirun = QPushButton('运行')

        self.currentFiletext = QLabel('当前文件: ')
        self.currentFile_diaplay = QLabel('  ')
        # self.currentFile_diaplay.setStyleSheet('font-size:22px')  # 这里样式的写法是好使的,写成'{font-size:22px}'不好使
        # self.currentFile_diaplay.setStyleSheet('padding-right:50px')
        self.scheduletext = QLabel('进度:     ')
        self.scheduletext.setStyleSheet('{margin-right:30px}')
        self.averageText = QLabel('平均准确率:       ')
        # self.averageText.setMinimumWidth(70)
        # self.averageText.setStyleSheet('width:70px')
        # self.averageText.setStyleSheet('margin-right:50px')

        # jpg = QPixmap('fruitkatong.jpg')

        jpg = QPixmap('fruitkatong.jpg').scaled(650, 320)
        self.label_image.setPixmap(jpg)

        self.layout.addWidget(self.label_singleimg, 0, 1, 1, 1)
        self.layout.addWidget(self.label_image, 1, 1, 4, 2)  # 将上面创建的一系列标签按追加到界面中,并设置显示位置
        self.layout.addWidget(self.button_search_image, 1, 3, 1, 2)
        self.layout.addWidget(self.button_run, 2, 3, 1, 2)
        self.layout.addWidget(self.label_predict_result, 3, 3, 1, 1)
        self.layout.addWidget(self.label_predict_result_display, 3, 4, 1, 1)
        self.layout.addWidget(self.label_predict_acc, 4, 3, 1, 1)
        self.layout.addWidget(self.label_predict_acc_display, 4, 4, 1, 1)

        # self.layout.addWidget(self.button_cover, 8, 4, 1, 1)

        self.layout.addWidget(self.label_multiimg, 7, 1, 1, 1)
        self.layout.addWidget(self.button_dir_display, 8, 1, 1, 3)
        self.layout.addWidget(self.button_search_dir, 8, 4, 1, 1)
        self.layout.addWidget(self.button_savedir_display, 9, 1, 1, 3)
        self.layout.addWidget(self.button_save_dir, 9, 4, 1, 1)
        self.layout.addWidget(self.ratetext, 10, 1, 1, 1)
        self.layout.addWidget(self.rate_slider, 10, 2, 1, 1)
        self.layout.addWidget(self.ratetext_display, 10, 3, 1, 1)
        self.layout.addWidget(self.button_multirun, 10, 4, 1, 1)

        self.layout.addWidget(self.currentFiletext, 11, 1, 1, 1)
        self.layout.addWidget(self.currentFile_diaplay, 11, 2, 1, 1)
        self.layout.addWidget(self.scheduletext, 11, 3, 1, 1)
        self.layout.addWidget(self.averageText, 11, 4, 1, 1)

        self.layout.setRowMinimumHeight(0, 30)
        # self.layout.setColumnMinimumWidth(0, 30)
        global filename
        filename = ''
        global dirname
        dirname = ''
        global savedirname
        savedirname = ''
        global currentRate
        currentRate = self.rate_slider.value()
        self.button_search_image.clicked.connect(lambda: self.openimage())
        self.button_run.clicked.connect(lambda: self.run())
        self.button_search_dir.clicked.connect(lambda: self.openimagedir())
        self.button_save_dir.clicked.connect(lambda: self.saveimgdir())
        self.rate_slider.valueChanged.connect(lambda: self.ratechange())
        # 对运行按钮执行运行函数 self.openimage self.run指本类函数
        self.button_multirun.clicked.connect(lambda: self.multirun())

        self.setLayout(self.layout)

        # self.show()  # 显示窗口

    def openimage(self):
        print('self.label_image:{}'.format(self.label_image))
        global filename

        imgName, imgType = QFileDialog.getOpenFileName(self, "选择图片", "", "*.jpg;;*.png")  # imgName返回文件绝对路径
        # imgType返回文件类型即拓展名
        # print('imgName:{}'.format(imgName))
        # print('imgType:{}'.format(imgType))
        # print(label_image.width())
        # print(label_image.height())
        print('type(imgName):{}'.format(type(imgName)))
        filename = imgName
        if len(filename) == 0:
            jpgfile = QPixmap('fruitkatong.jpg').scaled(640, 320)
            self.label_image.setPixmap(jpgfile)
        else:
            jpgfile = QPixmap(imgName).scaled(self.label_image.width(), self.label_image.height())
            # self.stack1UI()
            self.label_image.setPixmap(jpgfile)

            print('filename:{}'.format(filename))
            print('len(filename):{}'.format(len(filename)))

    def run(self):
        print('filename:{}'.format(filename))
        print('len(filename):{}'.format(len(filename)))
        if len(filename) == 0:
            # QMessageBox.warning(self, "文件错误", "请先选择文件后再运行", )
            mesBox = QMessageBox()
            mesBox.setWindowTitle('文件错误')
            mesBox.setText('请先选择文件后再运行')
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setStyleSheet('QMessageBox{color:black}')
            mesBox.exec_()  # 这句必须有，否则不出弹窗
        else:
            img = Image.open(filename)
            className, predictRate = predictclass.predict(img)
            self.label_predict_result_display.setText(className)  # 此时可以说明python传递类似java的对象数据，即可修改的数据时，修改后原来函数里的对应数据也会改变
            Rate = str(predictRate)
            Rate = float(Rate)
            print(Rate)
            self.label_predict_acc_display.setText(str(Rate * 100)[0:5] + ' %')

    def openimagedir(self):
        global dirname
        dirname = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.button_dir_display.setText(dirname)

    def saveimgdir(self):
        global savedirname
        savedirname = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.button_savedir_display.setText(savedirname)

    def multirun(self):
        # 转换思路 不行槽函数运行时在按钮上加点东西 给他遮上 让他点不了
        print(11)
        if len(dirname) == 0 or len(savedirname) == 0:
            # QMessageBox.warning(self, "文件夹错误", "目标文件夹或保存结果文件夹未选择")
            mesBox = QMessageBox()
            mesBox.setWindowTitle('文件夹错误')
            mesBox.setText('目标文件夹或保存结果文件夹未选择')
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setStyleSheet('QMessageBox{color:black}')
            mesBox.exec_()  # 这句必须有，否则不出弹窗
        else:
            print(222)
            self.averageText.setText('平均准确率:       ')
            self.button_multirun.setText('运行中')  # 主页面按钮点击后更新按钮文本
            self.button_multirun.setEnabled(False)  # 将按钮设置为不可点击
            self.Thread = ClassMulti()

            self.Thread.currentFile.connect(self.getCurrentfile)
            self.Thread.over.connect(self.over)
            self.Thread.start()

    def ratechange(self):
        self.ratetext_display.setText(str(self.rate_slider.value()) + ' %')
        global currentRate
        currentRate = str(self.rate_slider.value())

    def over(self, averageRate):
        self.averageText.setText('平均准确率: ' + averageRate + '%')  # 信号发过来时，更新QLabel内容
        self.button_multirun.setText('运行')  # 更新按钮
        self.button_multirun.setEnabled(True)  # 让按钮恢复可点击状态

    def getCurrentfile(self, currentfile, currentfilenum):
        global totalFile
        self.currentFile_diaplay.setText(currentfile)
        self.scheduletext.setText('进度:' + str(currentfilenum) + '/' + totalFile)
        # if str(currentfilenum) == totalFile:
        #     self.button_multirun.setText('运行')  # 更新按钮
        #     self.button_multirun.setEnabled(True)  # 让按钮恢复可点击状态


# class CalSumTheard(QThread):
#     """该线程用于计算耗时的累加操作"""
#     _sum = pyqtSignal(str)  # 信号类型 str
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#         s, k = 0, 0
#         while k <= 50000000:
#             s += k
#             k += 1
#         self._sum.emit(str(s))  # 计算结果完成后，发送结果


class ClassMulti(QThread):
    # currentFile = pyqtSignal(str)
    currentFile = pyqtSignal(str, str)
    over = pyqtSignal(str)  # 信号类型 str

    def __init__(self):
        super().__init__()

    def run(self):
        # threadSanUI1 = SanUI1()
        # rate = int(self.ratetext_display.text())
        # global currentRate
        rate = int(currentRate)
        print('线程rate:{}'.format(rate))

        # print(rate)
        # print('type(rate):{}'.format(type(rate)))
        images_path = glob.glob(
            os.path.join(dirname, '*.[jp][pn]g'))
        print('type(images_path):{}'.format(type(images_path)))
        print('len(images_path):{}'.format(len(images_path)))
        print(images_path)
        global totalFile
        totalFile = str(len(images_path))
        classDir = predictclass.class_indict
        predictRate = 0
        for createdirName in classDir.values():
            if not os.path.exists(savedirname + '/' + createdirName):
                os.mkdir(savedirname + '/' + createdirName)
            # print(createdirName)
            # print(savedirname + '/' + createdirName)
        if not os.path.exists(savedirname + '/' + '低于识别准确率下限'):
            os.mkdir(savedirname + '/' + '低于识别准确率下限')
        for current, image in enumerate(images_path):

            image = image.replace('\\', '/')  # 不加这个当前路径和文件名的杠会被转义
            print('image: %s' % image)
            currentFile = image.split('/')[-1]
            # print('current:{}'.format(current))
            self.currentFile.emit(currentFile, str(current + 1))
            # currentFile_diaplay.setText(str(current))
            # print('currentFile:{}'.format(currentFile))
            img = Image.open(image)
            className, predictRateStr = predictclass.predict(img)
            # print('type(predictRate):{}'.format(type(predictRateStr)))
            # print(predictRate)
            print('float(predictRateStr) %s' % float(predictRateStr))
            print(savedirname + '/' + className)
            if float(predictRateStr) * 100 > rate:
                shutil.copy(image, savedirname + '/' + className)
            else:
                shutil.copy(image, savedirname + '/' + '低于识别准确率下限')
            predictRate += float(predictRateStr) * 100

        predictRate = round(predictRate / int(totalFile), 2)
        print('predictRate:{}'.format(predictRate))
        for diritem in os.listdir(savedirname):
            if os.path.isdir(os.path.join(savedirname, diritem)):
                if len(os.listdir(os.path.join(savedirname, diritem))) == 0:
                    print(diritem)
                    os.removedirs(os.path.join(savedirname, diritem))
        self.over.emit(str(predictRate))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = SanUI1()
    sys.exit(app.exec_())
