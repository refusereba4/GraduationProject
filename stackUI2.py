# coding=utf-8
import glob
import os
import shutil
import sys

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout, QSlider, QFileDialog,
                             QMessageBox, QTextEdit)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import predictclass
import predictlabel


class SanUI2(QWidget):
    """基础Gui页面"""

    def __init__(self):
        super().__init__()
        self.init_ui()  # 主窗口

    def init_ui(self):
        # self.setGeometry(300, 300, 600, 200)  # 设置主窗口的位置和大小
        self.layout = QGridLayout()

        self.setStyleSheet(
            'QLabel{font-size:18px;}'
            'QPushButton{font-size:12px;background:rgb(255,223,140);}'
            'QMessageBox{color:black;font-size:10px}'

        )

        self.label_singleimg = QLabel('单图模式:')

        self.label_image = QLabel()  # 选择图片后显示图片的标签
        self.label_image.setStyleSheet('padding-right:100px')
        global predict_resultstr
        # predict_resultstr = '识别结果:\n'+'种类\t'+'概率\t'+'左上坐标\t'+'右下坐标\n'
        predict_resultstr = '识别结果:\n' + '{:^15}\t{:^15}\t{:^25}\t{:^25}\n'.format('Category', 'Accuracy',
                                                                                  'Upper left coordinate',
                                                                                  'Bottom right coordinate')
        # self.label_predict_result = QLabel(predict_resultstr)  # 识别结果文本提示标签
        self.label_predict_result = QTextEdit()
        self.label_predict_result.setReadOnly(True)  # 文本区域只读 禁止用户编辑 就是文本框里没有光标了 但是鼠标拖动还是可以复制内容
        self.label_predict_result.setMinimumWidth(100)

        self.label_predict_result.setPlainText(predict_resultstr)
        # self.label_predict_result.setMaximumHeight(45)
        self.label_predict_result.setStyleSheet('font-size:18px')
        self.label_predict_result_display = QLabel()  # 识别结果标签

        self.button_search_image = QPushButton('选择图片')  # 选择图片的文本提示标签
        self.button_run = QPushButton('运行')  # 运行标签

        self.button_savimg = QPushButton('保存图片')
        self.button_savdata = QPushButton('保存结果数据')

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
            'QSlider::handle:horizontal{width:20px;background-color:rgb(255,255,255);margin:-9px 0px -9px '
            '0px;border-radius:10px;}'
            "QSlider::groove:horizontal{height:5px;background-color:rgb(219,219,219);}"
            "QSlider::add-page:horizontal{background-color:rgb(219,219,219);}"
            "QSlider::sub-page:horizontal{background-color:rgb(26,217,110);}"
        )
        self.rate_slider.setRange(50, 90)
        self.rate_slider.setValue(85)
        self.rate_slider.setSingleStep(5)

        self.button_multirun = QPushButton('运行')
        self.button_multirun.setStyleSheet('{margin-bottom:50px}')

        self.currentFiletext = QLabel('当前文件: ')
        self.currentFile_diaplay = QLabel('  ')

        self.scheduletext = QLabel('进度:     ')
        self.scheduletext.setStyleSheet('{margin-right:30px}')
        self.averageText = QLabel('平均准确率:       ')

        jpg = QPixmap('fruitkatong.jpg').scaled(650, 300)
        self.label_image.setPixmap(jpg)

        self.layout.addWidget(self.label_singleimg, 0, 1, 1, 1)
        self.layout.addWidget(self.label_image, 1, 1, 2, 2)  # 将上面创建的一系列标签按追加到界面中,并设置显示位置
        self.layout.addWidget(self.button_search_image, 1, 3, 1, 2)
        self.layout.addWidget(self.button_run, 2, 3, 1, 2)
        self.layout.addWidget(self.label_predict_result, 3, 1, 3, 3)
        # self.layout.addWidget(self.label_predict_result_display, 4, 3, 3, 2)
        self.layout.addWidget(self.button_savimg, 3, 4, 1, 1)
        self.layout.addWidget(self.button_savdata, 4, 4, 1, 1)
        self.layout.addWidget(self.label_multiimg, 7, 1, 1, 1)
        self.layout.addWidget(self.button_dir_display, 8, 1, 1, 3)
        self.layout.addWidget(self.button_search_dir, 8, 4, 1, 1)
        self.layout.addWidget(self.button_savedir_display, 9, 1, 1, 3)
        self.layout.addWidget(self.button_save_dir, 9, 4, 1, 1)
        # self.layout.addWidget(self.ratetext, 10, 1, 1, 1)
        # self.layout.addWidget(self.rate_slider, 10, 2, 1, 1)
        self.layout.addWidget(self.button_multirun, 10, 4, 1, 1)

        self.layout.addWidget(self.currentFiletext, 11, 1, 1, 1)
        self.layout.addWidget(self.currentFile_diaplay, 11, 2, 1, 1)
        self.layout.addWidget(self.scheduletext, 11, 3, 1, 1)

        # self.layout.setColumnMinimumWidth(2,200)

        global filename
        filename = ''
        global dirname
        dirname = ''
        global savedirname
        savedirname = ''
        global currentRate
        currentRate = self.rate_slider.value()
        self.button_search_image.clicked.connect(lambda: self.openimage())
        self.button_search_dir.clicked.connect(lambda: self.openimagedir())
        self.button_save_dir.clicked.connect(lambda: self.saveimgdir())
        self.rate_slider.valueChanged.connect(lambda: self.ratechange())
        # # print('传回来的jpg:{}'.format(jpg))
        self.button_run.clicked.connect(lambda: self.run())
        # 对运行按钮执行运行函数 self.openimage self.run指的应该是本类函数
        self.button_multirun.clicked.connect(lambda: self.multirun())

        self.button_savimg.clicked.connect(lambda: self.singleimgsave())
        self.button_savdata.clicked.connect(lambda: self.singledatasave())

        self.setLayout(self.layout)

        # self.show()  # 显示窗口

    def openimage(self):
        print('self.label_image:{}'.format(self.label_image))
        global filename

        imgName, imgType = QFileDialog.getOpenFileName(self, "选择图片", "", "*.jpg;;*.png")  # imgName返回文件绝对路径
        print('type(imgName):{}'.format(type(imgName)))
        global predict_resultstr
        predict_resultstr = '识别结果:\n' + '{:^15}\t{:^15}\t{:^25}\t{:^25}\n'.format('Category', 'Accuracy',
                                                                                  'Upper left coordinate',
                                                                                  'Bottom right coordinate')
        self.label_predict_result.setPlainText(predict_resultstr)
        # print('正常识别结果字符串长度：{}'.format(len(predict_resultstr)))
        filename = imgName
        if len(filename) == 0:
            jpgfile = QPixmap('fruitkatong.jpg').scaled(650, 300)
            self.label_image.setPixmap(jpgfile)
        else:
            jpgfile = QPixmap(imgName).scaled(650, 300)
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
            returnList, returnlabelimg = predictlabel.predictsingle(img)
            global labelimg
            labelimg = returnlabelimg

            # self.label_predict_result_display.setText(returnList[0]+'\n'+returnList[0]+'\n')
            global predict_resultstr
            global predict_resultstrtxt
            predict_resultstr = '识别结果:\n' + '{:^15}\t{:^15}\t{:^25}\t{:^25}\n'.format('Category', 'Accuracy',
                                                                                      'Upper left coordinate',
                                                                                      'Bottom right coordinate')
            predict_resultstrtxt = '识别结果:\n' + '{:^15}\t{:^15}\t{:^30}\t{:^30}\n'.format('Category', 'Accuracy',
                                                                                         'Upper left coordinate',
                                                                                         'Bottom right coordinate')

            for stritem in returnList:
                predict_resultstr += '{:^15}\t{:^15}\t{:^25}\t{:^25}\n'.format(stritem[0], stritem[1], stritem[2],
                                                                               stritem[3])
                predict_resultstrtxt += '{:^15}\t{:^15}\t{:^30}\t{:^30}\n'.format(stritem[0], stritem[1], stritem[2],
                                                                               stritem[3])

            self.label_predict_result.setText(predict_resultstr)
            # 此时可以说明python传递类似java的对象数据，即可修改的数据时，修改后原来函数里的对应数据也会改变
            # Rate = str(predictRate)
            # Rate = float(Rate)
            # print(Rate)
            # self.label_predict_acc_display.setText(str(Rate * 100)[0:5] + ' %')

    def singleimgsave(self):
        global labelimg
        # labelimg.
        print('labelimg:{}'.format(labelimg))
        print('type(labelimg):{}'.format(type(labelimg)))
        global filename
        global predict_resultstr
        if len(filename) == 0 or len(predict_resultstr) < 95:
            mesBox = QMessageBox()
            mesBox.setWindowTitle('文件错误')
            mesBox.setText('请先运行后再保存')
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setStyleSheet('QMessageBox{color:black}')
            mesBox.exec_()  # 这句必须有，否则不出弹窗
        else:
            saveimgname = QFileDialog.getSaveFileName(None, '选择保存图片路径', 'C:/', '*.jpg;;*.png')
            print('filename:{}'.format(saveimgname))
            print(saveimgname[0])
            print(len(saveimgname[0]))
            if len(saveimgname[0]) != 0:
                labelimg.save(saveimgname[0])

    def singledatasave(self):
        global filename
        global predict_resultstrtxt
        if len(filename) == 0 or len(predict_resultstr) < 95:
            mesBox = QMessageBox()
            mesBox.setWindowTitle('文件错误')
            mesBox.setText('请先运行后再保存')
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setStyleSheet('QMessageBox{color:black}')
            mesBox.exec_()  # 这句必须有，否则不出弹窗
        else:
            savedataname = QFileDialog.getSaveFileName(None, '选择识别结果保存路径', 'D:/', '*.txt;')
            print('filename:{}'.format(savedataname))
            print(savedataname[0])
            print(len(savedataname[0]))
            print(type(predict_resultstr))
            if len(savedataname[0]) != 0:
                fp = open(savedataname[0], 'w')
                fp.write(predict_resultstrtxt)
                fp.close()

    def openimagedir(self):
        global dirname
        dirname = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.button_dir_display.setText(dirname)

    def saveimgdir(self):
        global savedirname
        savedirname = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.button_savedir_display.setText(savedirname)

    def multirun(self):
        if len(dirname) == 0 or len(savedirname) == 0:
            # QMessageBox.warning(self, "文件夹错误", "目标文件夹或保存结果文件夹未选择")
            mesBox = QMessageBox()
            mesBox.setWindowTitle('文件夹错误')
            mesBox.setText('目标文件夹或保存结果文件夹未选择')
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setStyleSheet('QMessageBox{color:black}')
            mesBox.exec_()  # 这句必须有，否则不出弹窗
        else:
            self.averageText.setText('平均准确率:       ')
            self.button_multirun.setText('运行中')  # 主页面按钮点击后更新按钮文本
            self.button_multirun.setEnabled(False)  # 将按钮设置为不可点击
            self.Thread = LabelMulti()

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


class LabelMulti(QThread):
    currentFile = pyqtSignal(str, str)
    over = pyqtSignal(str)  # 信号类型 str

    def __init__(self):
        super().__init__()

    def run(self):
        rate = int(currentRate)
        # print('线程rate:{}'.format(rate))
        images_path = glob.glob(
            os.path.join(dirname, '*.[jp][pn]g'))
        print('type(images_path):{}'.format(type(images_path)))
        print('len(images_path):{}'.format(len(images_path)))
        print(images_path)
        print('savedirname:{}'.format(savedirname))
        global totalFile
        totalFile = str(len(images_path))
        classDir = predictclass.class_indict
        predictRate = 0
        for current, image in enumerate(images_path):

            image = image.replace('\\', '/')  # 不加这个当前路径和文件名的杠会被转义
            print('image: %s' % image)
            currentFile = image.split('/')[-1]
            print('current:{}'.format(current))
            self.currentFile.emit(currentFile, str(current + 1))

            img = Image.open(image)
            returnList, returnlabelimg = predictlabel.predictmulti(img)
            global labelimg
            labelimg = returnlabelimg
            # print(returnList)
            # print(returnList[0])
            labelimg.save(os.path.join(savedirname, currentFile))
            # self.label_predict_result_display.setText(returnList[0]+'\n'+returnList[0]+'\n')
            global predict_resultstr
            predict_resultstr = '识别结果:\n' + '{:^15}\t{:^15}\t{:^30}\t{:^30}\n'.format('Category', 'Accuracy',
                                                                                      'Upper left coordinate',
                                                                                      'Bottom right coordinate')
            # returnstr = ''
            for stritem in returnList:
                predict_resultstr += '{:^15}\t{:^15}\t{:^30}\t{:^30}\n'.format(stritem[0], stritem[1], stritem[2],
                                                                               stritem[3])
            fp = open(os.path.join(savedirname, currentFile) + '.txt', 'w')
            fp.write(predict_resultstr)
            fp.close()

        self.over.emit(str(predictRate))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = SanUI2()
    sys.exit(app.exec_())
