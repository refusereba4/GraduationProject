import sys

# 使用调色板等
from PyQt5.QtGui import QIcon
# 导入QT,其中包含一些常量，例如颜色等
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout


from stackUI1 import SanUI1
from stackUI2 import SanUI2
from stackUI3 import SanUI3
from stackUI4 import SanUI4


class DemoWin(QWidget):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()

    def initUI(self):
        # 将窗口设置为动图大小
        self.setFixedSize(600, 300)

        self.list = QListWidget()
        self.list.setMaximumWidth(100)

        # 设置列表内容（stack的索引）
        self.list.insertItem(0, '水果图片分类')
        self.setStyleSheet(
            'QListWidget:focus{outline:none}'
            'QListWidget::Item{padding-top:20px;outline:none}'
            'QListWidget::Item:selected{background:rgb(255,223,140);border-width:0px;padding:0.1;color:black}'
        )
        self.clearFocus()
        self.list.insertItem(1, '水果图片标注')
        selectItem = self.list.item(0)

        selectItem.setSelected(True)  # 默认选中第一项
        self.list.insertItem(2, '水果实时标注')
        self.list.insertItem(3, '使用说明')
        # 创建三个stack页面
        self.stack1 = SanUI1()
        self.stack2 = SanUI2()
        self.stack3 = SanUI3()
        self.stack4 = SanUI4()

        # 将三个stack页面加入stackWidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.addWidget(self.stack1)
        self.stackWidget.addWidget(self.stack2)
        self.stackWidget.addWidget(self.stack3)
        self.stackWidget.addWidget(self.stack4)

        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addWidget(self.stackWidget)
        self.setLayout(hbox)

        # 为List绑定事件，当条目改变时，切换stack（重要）
        self.list.currentRowChanged.connect(self.stackSwitch)

        # 添加窗口标题
        self.setWindowTitle("水果图片分类标注系统")

    # 切换list时触发槽函数切换Stack
    def stackSwitch(self, index):
        self.stackWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.jpg"))
    # 创建一个主窗口
    mainWin = DemoWin()
    mainWin.setFixedSize(1180, 700)

    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())
