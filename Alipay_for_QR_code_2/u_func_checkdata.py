# ui_checkdata_1.py 用到的自定义函数

import copy
import os

import pymysql
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np

db = pymysql.connect('ip', 'root', 'pwd', 'databases', charset='utf8')
cur = db.cursor()


def caipinfenxi(pb_txt, dt, db):
    # 菜品数目分析函数
    if os.path.exists('caipinfengxi.png'):
        os.remove('caipinfengxi.png')
    # pb_txt = 'today'
    # dt = ['2020', '5', '9']

    cur = db.cursor()
    # 筛选日
    day1, day2 = '', ''
    if pb_txt == 'today':
        day1 = [dt[0], dt[1], str(int(dt[-1]))]
        day2 = [dt[0], dt[1], str(int(dt[-1]) + 1)]
        new_time = '今日'
    elif pb_txt == 'week':
        day1 = [dt[0], dt[1], str(int(dt[-1]) - 6)]
        day2 = [dt[0], dt[1], str(int(dt[-1]) + 1)]
        new_time = "本周"
    elif pb_txt == 'mouth':
        day1 = [dt[0], dt[1], '1']
        day2 = [dt[0], str(int(dt[1]) + 1), '1']
        new_time = '本月'
    dt1 = '-'.join(day1)
    dt2 = '-'.join(day2)
    # print(dt1, '-'.join(dt), dt2)
    sql = f"select * from order_menu_list where time>'{dt1}' and time<'{dt2}'"
    cur.execute(sql)
    data = cur.fetchall()
    # print(data)
    # data 为 筛选出的数据

    menu = []
    good_id = []
    # 整理data 具体菜单
    for item1 in data:
        a1 = item1[2].split(',')
        for i, item2 in enumerate(a1):
            item2 = item2.split('x')
            a1[i] = [int(item2[0]), int(item2[1])]

            if len(good_id) == 0:
                good_id.append(int(item2[0]))
            elif int(item2[0]) not in good_id:
                good_id.append(int(item2[0]))
            # 统计有效id
        menu.append(a1)
    # for item in menu:
    #     print(item)
    # print(good_id)
    # 可以 def
    # 统计一天内的菜品和数量
    gxn = []
    menu_copy1 = copy.deepcopy(menu)
    for i, item1 in enumerate(good_id):
        a = 0
        for j, item2 in enumerate(menu_copy1):
            for k, item3 in enumerate(item2):
                if len(item3):
                    if item1 == item3[0]:
                        a += item3[1]
                        item3.clear()
        gxn.append([item1, a])
    # print(gxn)
    # 菜品id -> name
    x, y = [], []
    p = 0
    good_name = ['', '']    # [max, min]
    good_n = [0, 5]
    good_p = [0, 50]

    for item in gxn:
        sql2 = f"select * from good_list where id='{item[0]}'"
        cur.execute(sql2)
        data = cur.fetchone()  # data[id,name,price,size]
        x.append(str(data[1]))
        y.append(item[1])
        p += int(data[2]) * item[1]  # 统计价格
        if good_n[0] < int(item[1]):
            good_n[0] = int(item[1])
            good_p[0] = int(data[2]) * item[1]
            good_name[0] = data[1]

        if good_n[1] > int(item[1]):
            good_n[1] = int(item[1])
            good_p[1] = int(data[2]) * item[1]
            good_name[1] = data[1]

    # print(x)
    # print(y)
    # print(p)
    fener_max = good_p[0] * 100 / p
    fener_min = good_p[1] * 100 / p

    print(f'{new_time}的建议：')
    print(f'\t{good_name[0]} 菜品售出最多，有{fener_max:0.2f}%的占比，{good_name[1]} 菜品售出最少，有{fener_min:0.2f}%的占比')
    # 绘制图
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(x=x, height=y)
    plt.title(f'{new_time}售卖')
    plt.xlabel('菜品')
    plt.ylabel('数目/份')

    plt.savefig(r'caipinfengxi.png')
    return p
    pass


def jingrongzoushi(pb_txt, dt, db):
    # 金融走势函数
    if os.path.exists('jinrongzoushi.png'):
        os.remove('jinrongzoushi.png')
    # pb_txt = 'week'  # or 'mouth'
    # dt = ['2020', '5', '9']
    # print(pb_txt, dt)
    cur = db.cursor()
    # 处理日期区间
    day1, day2 = '', ''
    if pb_txt == 'week':
        day1 = [dt[0], dt[1], str(int(dt[-1]) - 6)]
        day2 = [dt[0], dt[1], str(int(dt[-1]) + 1)]
    elif pb_txt == 'mouth':
        day1 = [dt[0], dt[1], '1']
        day2 = [dt[0], str(int(dt[1]) + 1), '1']

    dt1 = '-'.join(day1)
    dt2 = '-'.join(day2)
    # print(dt1, '-'.join(dt), dt2)
    sql = f"select * from order_menu_list where time>'{dt1}' and time<'{dt2}'"
    cur.execute(sql)
    data = cur.fetchall()
    # print(data)
    # data 为 筛选出的数据
    # 整理data
    week_len = len(data)  # 前7 天数据库
    week_menu = []
    week_all_day = []
    # date
    dy = []
    for i in range(week_len - 1):
        d1 = int(str(data[i][3])[8:10])
        d2 = int(str(data[i + 1][3])[8:10])
        # print(d1, d2)
        if i == 0:
            dy.append(str(data[i][2]))
            week_all_day.append(d1)
            # print(dy)
        if d1 == d2:
            dy.append(str(data[i+1][2]))
            if i+1 == week_len-1:
                # print(dy)
                week_menu.append(dy)
        elif d1 != d2:
            week_all_day.append(d2)
            # print(dy)
            week_menu.append(dy)
            dy = [str(data[i + 1][2])]

    # print(week_menu)
    # print(week_all_day) # time
    # 统计利润
    week_one_money = []
    for i in range(len(week_all_day)):
        p = one_day_money(week_menu[i])
        week_one_money.append(p)
    # print(week_one_money)   # money

    # 绘制图
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(x=week_all_day, height=week_one_money)
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    new_time = ''
    if pb_txt == 'week':
        new_time = '本周'
    else:
        new_time = '本月'

    plt.title(f'{new_time}消费状况')
    plt.xlabel(f'{new_time}开张日期/day')
    plt.ylabel('每日售出/元')
    # plt.show()
    plt.savefig(r'jinrongzoushi.png')
    return sum(week_one_money)
    pass


def one_day_money(data):
    # 函数

    # 计算一天的 菜品 的一些数据
    # 当前只返回 一天盈利 数据
    # 可在程序后面自己扩展

    menu = []
    good_id = []
    # 整理data 具体菜单
    for item1 in data:
        a1 = item1.split(',')
        for i, item2 in enumerate(a1):
            item2 = item2.split('x')
            a1[i] = [int(item2[0]), int(item2[1])]

            if len(good_id) == 0:
                good_id.append(int(item2[0]))
            elif int(item2[0]) not in good_id:
                good_id.append(int(item2[0]))
            # 统计有效id
        menu.append(a1)
    # for item in menu:
    #     print(item)
    # print(good_id)
    # 可以 def
    # 统计一天内的菜品和数量
    gxn = []
    menu_copy1 = copy.deepcopy(menu)
    for i, item1 in enumerate(good_id):
        a = 0
        for j, item2 in enumerate(menu_copy1):
            for k, item3 in enumerate(item2):
                if len(item3):
                    if item1 == item3[0]:
                        a += item3[1]
                        item3.clear()
        gxn.append([item1, a])
    # print(gxn)
    # 菜品id -> name
    x, y = [], []
    p = 0
    for item in gxn:
        sql2 = f"select * from good_list where id='{item[0]}'"
        cur.execute(sql2)
        data = cur.fetchone()  # data2[id,name,price,size]
        x.append(str(data[1]))
        y.append(item[1])
        p += int(data[2]) * item[1]  # 统计价格
    # print(x)  # name
    # print(y)  # shuliang
    # print(p)  # ying li
    return p


if __name__ == '__main__':

    print('-----链接数据库------')
    db = pymysql.connect('ip', 'root', 'pwd', 'databases', charset='utf8')
    cur = db.cursor()

    # p = caipinfenxi(dt, db)
    p = jingrongzoushi(pb_txt=0, dt=0, db=db)
