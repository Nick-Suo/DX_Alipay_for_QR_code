# ui 0.
# 数据分析ui


import sys
# from PyQt5.QtWidgets import QPushButton, QApplication, QWidget
import time

import pymysql
from PyQt5.Qt import *


from source.checkdata_1 import Ui_Form
from u_func_checkdata import caipinfenxi, jingrongzoushi


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("")      # 默认窗口设置
        self.setupUi(self)
        self.dt = ''    # riqi
        self.date = ''  # riqi
        self.p = 0      # lirong
        self.pb_txt = 'today'    # week or mouth
        # dateedit setting
        self.dateEdit.setDate(QDate(2020, 5, 9))

        self.init_widget()

    def init_widget(self):
        # 一些初始化状态

        # label setting
        self.label.clear()

        # lineEdit setting
        self.lineEdit.clear()
        # self.lineEdit_2.clear()

        # button setting
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)

        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(False)

    def dt_date_change(self, Date):
        # 调整日期 触发的槽
        print('-' * 5 + 'Date\t\t' + '-' * 5)
        dt = str(Date)[19:-1].split(', ')
        date = '-'.join(dt)
        self.dt = dt
        self.date = date
        print(dt, date)

    def pb_today_click(self):
        # 日 按钮被被点击触发槽
        self.init_widget()
        self.pushButton.setStyleSheet('background-color: cyan')
        self.pushButton_2.setStyleSheet('')
        self.pushButton_3.setStyleSheet('')
        self.pushButton_4.setStyleSheet('')
        self.pushButton_5.setStyleSheet('')

        # self.pushButton_5.setEnabled(False)
        print('-' * 5 + '今日份的数据\t\t' + '-' * 5)
        self.pb_txt = 'today'
        pass

    def pb_week_click(self):
        # 周 按钮被被点击触发槽
        self.init_widget()
        self.pushButton.setStyleSheet('')
        self.pushButton_2.setStyleSheet('background-color: cyan')
        self.pushButton_3.setStyleSheet('')
        self.pushButton_4.setStyleSheet('')
        self.pushButton_5.setStyleSheet('')
        self.pushButton_5.setEnabled(True)

        print('-' * 5 + '本周的数据\t\t\t' + '-' * 5)
        self.pb_txt = 'week'

        pass

    def pb_mouth_click(self):
        # 月 按钮被被点击触发槽
        self.init_widget()
        self.pushButton.setStyleSheet('')
        self.pushButton_2.setStyleSheet('')
        self.pushButton_3.setStyleSheet('background-color: cyan')
        self.pushButton_4.setStyleSheet('')
        self.pushButton_5.setStyleSheet('')
        self.pushButton_5.setEnabled(True)
        print('-' * 5 + '本月份的数据\t\t' + '-' * 5)
        self.pb_txt = 'mouth'
        pass

    def pb_caipingfenxitu_click(self):
        # 菜品分析 按钮被被点击触发槽
        self.pushButton_4.setStyleSheet('background-color: cyan')
        self.pushButton_5.setStyleSheet('')
        print('-' * 5 + '菜品分析\t\t' + '-' * 5)

        dt = self.dateEdit.text()
        self.dt = dt.split('/')

        self.p = caipinfenxi(self.pb_txt, self.dt, db)
        time.sleep(1)
        
        self.dt = ''

        self.lineEdit.setText(str(self.p))

        self.label.setScaledContents(True)  # 缩放图片大小为 label 大小
        self.label.setPixmap(QPixmap('caipinfengxi.png'))
        pass

    def pb_jingrongzoushi_click(self):
        # 金融走势 按钮被被点击触发槽
        self.pushButton_4.setStyleSheet('')
        self.pushButton_5.setStyleSheet('background-color: cyan')
        print('-' * 5 + '金融走势\t\t' + '-' * 5)
        dt = self.dateEdit.text()
        self.dt = dt.split('/')

        p = jingrongzoushi(self.pb_txt, self.dt, db)
        time.sleep(1)

        self.lineEdit.setText('')
        self.lineEdit.setText(str(p))
        self.label.setPixmap(QPixmap(''))

        self.label.setScaledContents(True)  # 缩放图片大小为 label 大小
        self.label.setPixmap(QPixmap('jinrongzoushi.png'))

        pass


if __name__ == '__main__':
    # read me
    # 这是数据分析ui ，build版 0.1，
    # 实现功能介绍
    # 按照菜品具体售出的情况， 从售出菜品的数量、每日盈利发展开数据分析

    # 分为 按日、周、月时间进行统计数据， 并以图表具体显示
    # 日：      主要分析当天售出所有的菜品数据， 并绘制为具体菜品的柱状图，跟直观的看到所有菜品售出情况
    #           以及展示盈利金额

    # 周：      也会统计当周售出的菜品数据，
    #           增加了分析每日具体的盈利状况

    # 月：        周 的扩展数据

    # ----------
    # 连接数据库
    db = pymysql.connect('175.24.87.13', 'shuike', '123456', 'shuikedatabase', charset='utf8')
    cur = db.cursor()

    # -----------
    # ui展示
    app = QApplication(sys.argv)  # sys.argv 反馈窗口输入
    window = Window()
    window.show()               # 窗口显示
    sys.exit(app.exec_())  # app.exec_() 保持窗口刷新 sys.exit反馈错误类型

