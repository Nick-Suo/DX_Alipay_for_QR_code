import sys
# from PyQt5.QtWidgets import QPushButton, QApplication, QWidget
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("")      # 默认窗口设置
        self.setGeometry(300, 300, 350, 350)
        # self.Desktop_ui()

    def Desktop_ui(self):
        pb1 = QRadioButton('1', self)
        pb2 = QRadioButton('2', self)

        bg = QButtonGroup(self)
        bg.addButton(pb1)
        bg.addButton(pb2)

        ml = QHBoxLayout(self)
        ml.setSpacing(0)
        ml.addWidget(pb1)
        ml.addWidget(pb2)



if __name__ == '__main__':

    app = QApplication(sys.argv)  # sys.argv 反馈窗口输入
    window = Window()
    window.show()               # 窗口显示
    sys.exit(app.exec_())  # app.exec_() 保持窗口刷新 sys.exit反馈错误类型
