import pymysql
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os


def get_dbdata():
    cur = db.cursor()
    li = []
    for i in range(1, 4):
        sql = f'select * from tdlas_tdlas_data_gen2 where PreSet_Point="{i}" && Tdlas_Data_Err_Code="0";'
        cur.execute(sql)
        data = cur.fetchall()
        result = []
        PreSet_Point = []
        Rec_Date = []

        RESULT_p = [0, 0, 0, 0]  # <100 100<x<500 500<x<1000 1000<x
        for item in data:
            result.append(item[3])
            if item[3] <= 100:
                RESULT_p[0] += 1
            elif item[3] <= 500:
                RESULT_p[1] += 1
            elif item[3] <= 1000:
                RESULT_p[2] += 1
            elif item[3] > 1000:
                RESULT_p[3] += 1
            Rec_Date.append(item[-1])
        li.append(RESULT_p)

    print(li)

    def auto_text(rects):
        for rect in rects:
            ax.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    barWidth = 0.25
    x = ["<100", "100-500", "500-1000", ">1000"]
    r1 = np.arange(len(x))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    fig, ax = plt.subplots()
    plt.title("7日内所有正常result值分布")
    rect1 = ax.bar(r1, li[0], color='#FF0088', width=barWidth, edgecolor='white', label='点位1')
    rect2 = ax.bar(r2, li[1], color='#00BBFF', width=barWidth, edgecolor='white', label='点位2')
    rect3 = ax.bar(r3, li[2], color='#FF5511', width=barWidth, edgecolor='white', label='点位3')
    auto_text(rect1)
    auto_text(rect2)
    auto_text(rect3)
    plt.xticks([r + barWidth for r in range(len(x))], x)
    plt.legend()

    #plt.savefig("7日内所有正常result值分布.png")


def get_err_data():
    cur = db.cursor()
    li = []
    a = 0
    for m in range(0,8):
        err_ = [0, 0, 0]  # 2,4,20
        for i in range(1, 4):
            Point_errcode = []

            for j,err in enumerate([2,4,20]):
                sql = f'select * from tdlas_tdlas_data_gen2 where PreSet_Point="{i}" && Tdlas_Data_Err_Code="{err}"&&Rec_Date>="2021-04-{6+m} 00:00:00"&&Rec_Date<="2021-04-{6+m} 23:59:59";'
                cur.execute(sql)
                data = cur.fetchall()
                err_[j] += len(data)
                a += len(data)
        li.append(err_)
    print(li, a)
    li_1 = []
    li_2 = []
    li_3 = []
    for item in li:
        li_1.append(item[0])
        li_2.append(item[1])
        li_3.append(item[2])

    def auto_text(rects):
        for rect in rects:
            ax.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    barWidth = 0.25
    x = [6,7,8,9,10,11,12,13]
    r1 = np.arange(len(x))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    fig, ax = plt.subplots()
    plt.title("7日内所有错误码分布")
    rect1 = ax.bar(r1, li_1, color='#FF0088', width=barWidth, edgecolor='white', label='错误码2')
    rect2 = ax.bar(r2, li_2, color='#00BBFF', width=barWidth, edgecolor='white', label='错误码4')
    rect3 = ax.bar(r3, li_3, color='#FF5511', width=barWidth, edgecolor='white', label='错误码20')
    plt.xticks([r + barWidth for r in range(len(x))], x)
    auto_text(rect1)
    auto_text(rect2)
    auto_text(rect3)

    plt.legend()
    plt.show()

if __name__ == '__main__':

    db = pymysql.connect("localhost", "root", "root", "tdlas", charset="utf8")

    get_dbdata()
    get_err_data()
