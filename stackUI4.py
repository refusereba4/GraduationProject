# coding=utf-8
import glob
import os
import shutil
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout, QSlider, QFileDialog,
                             QMessageBox)


class SanUI4(QWidget):
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
        self.label_fenlei = QLabel('水果图片分类:')
        self.label_fenlei.setStyleSheet('margin-left:0px')
        self.fenlei1 = QLabel('单图模式下先点击选择按钮选择图片，然后点击运行')
        self.fenlei2 = QLabel('多图模式下选择待检测图片所在目录及保存结果目录后，再点击运行')
        self.fenlei3 = QLabel('水果分类目前支持24种水果的目标分类，如下:')
        self.fenlei4 = QLabel('哈密瓜,山竹,杏,杨梅,柚子,柠檬,桃子,桑葚,梨子,樱桃,橙子,火龙果,\n'
                              '猕猴桃,石榴,芒果,苹果,草莓,荔枝,菠萝,葡萄,蓝莓,西瓜,香蕉,龙眼,')

        self.label_biaozhu = QLabel('水果图片标注:')
        self.label_biaozhu.setStyleSheet('margin-left:0px')
        self.biaozhu1 = QLabel('单图模式下先选择待检测图片后再运行')
        self.biaozhu2 = QLabel('检测运行后才可以保存标注后的图片以及结果数据')
        self.biaozhu3 = QLabel('多图模式下选择好待检测图片所在目录及保存结果目录后再运行')
        self.biaozhu4 = QLabel('水果标注目前支持5种水果的标注，如下:')
        self.biaozhu5 = QLabel('苹果,香蕉,橙子,草莓,猕猴桃')

        self.label_camera = QLabel('水果实时标注:')
        self.label_camera.setStyleSheet('margin-left:0px')
        self.camera1 = QLabel('点击开启检测按钮，会自动开启摄像头并显示画面开始检测，此时按钮内容变为“关闭检测”')
        self.camera2 = QLabel('点击关闭检测按钮，会自动关闭摄像头画面并释放摄像头资源')

        self.layout.addWidget(self.label_fenlei, 0, 1, 1, 1)
        self.layout.addWidget(self.fenlei1, 1, 1, 1, 1)
        self.layout.addWidget(self.fenlei2, 2, 1, 1, 1)
        self.layout.addWidget(self.fenlei3, 3, 1, 1, 1)
        self.layout.addWidget(self.fenlei4, 4, 1, 1, 1)
        self.layout.addWidget(self.label_biaozhu, 5, 1, 1, 1)
        self.layout.addWidget(self.biaozhu1, 6, 1, 1, 1)
        self.layout.addWidget(self.biaozhu2, 7, 1, 1, 1)
        self.layout.addWidget(self.biaozhu3, 8, 1, 1, 1)
        self.layout.addWidget(self.biaozhu4, 9, 1, 1, 1)
        self.layout.addWidget(self.biaozhu5, 10, 1, 1, 1)
        self.layout.addWidget(self.label_camera, 11, 1, 1, 1)
        self.layout.addWidget(self.camera1, 12, 1, 1, 1)
        self.layout.addWidget(self.camera2, 13, 1, 1, 1)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = SanUI3()
    sys.exit(app.exec_())
