import datetime

from cv2.dnn import DNN_BACKEND_INFERENCE_ENGINE, DNN_TARGET_CPU, DNN_BACKEND_OPENCV
import cv2 as cv
import os

import pymysql
import uuid


def load_md(graph_txt, inference_pb):
    # inference_pb = "frozen_inference_graph.pb"  # pb
    # graph_txt = "graph.pbtxt"                   # txt
    net = cv.dnn.readNetFromTensorflow(inference_pb, graph_txt)    # 旧版 需要手动在cv2文件夹里更换cv2.cp37-win_amd64.pyd      10fps
    # net = cv.dnn.readNetFromModelOptimizer(graph_xml, inference_bin)  # openvino 需要手动在cv2文件夹里更换cv2.pyd  60fps
    net.setPreferableBackend(DNN_BACKEND_INFERENCE_ENGINE)  # openvino加速    # 默认设置 可以不添加
    net.setPreferableTarget(DNN_TARGET_CPU)  # 。。
    return net


def read_img(url):
    img = cv.imread(url)
    # h, w = img.shape[:2]
    # img = cv.resize(img, (int(w/2), int(h/2)))
    detect = model_return(net, img)
    cv.imshow(url, img)
    cv.waitKey()
    cv.destroyAllWindows()
    return detect


def model_return(net, frame):
    good = []
    im_tensor = cv.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
    net.setInput(im_tensor)
    cvOut = net.forward()
    for detect in cvOut[0, 0, :, :]:
        detect = detect.tolist()  # numpy  ->  list
        score = detect[2]
        h, w = frame.shape[:2]
        detect[1] = int(detect[1])
        detect[2] = float(f"{detect[2] * 100 :.2f}")  # 统一概率格式 00.0
        detect[3] = float(f"{detect[3] * w :.2f}")
        detect[4] = float(f"{detect[4] * h :.2f}")
        detect[5] = float(f"{detect[5] * w :.2f}")
        detect[6] = float(f"{detect[6] * h :.2f}")
        if score > 0.91:
            img_box(detect, frame)
            detect.pop(0)
            good.append(detect)
    return good


def img_box(detect, frame):
    left = detect[3] + 50
    top = detect[4] + 50
    right = detect[5] - 50
    bottom = detect[6] - 50
    print(detect)
    cv.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 4)
    cv.putText(frame, str(int(detect[1])), (int(left), int(top)), 1, 0.9, (0, 255, 255), 1)


def make_menu(detect):
    name = ''
    for item in detect:     # [3, 99.93, 34.12, 50.62, 499.18, 447.5]
        name += str(item[0]) + 'x' + '1' + ','
    name = name[:-1]
    print(name)
    no = uuid.uuid4()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    # 系统时间

    data = [str(no), name, now_time]
    return data


def menu_mysql(data):
    print(data)
    sql0 = "select * from order_menu_list order by id desc limit 1;"
    cur.execute(sql0)
    row_last = cur.fetchall()
    # print(row_last)

    id = int(row_last[0][0])
    no = data[0]
    menu = data[1]
    time = data[2]
    sql = f"insert into order_menu_list (id, no, menu, time) values (%s,%s,%s,%s)"
    # cur.execute(sql, (id + 1, no, menu, time))
    cur.execute(sql, (id + 1, id + 1, menu, time))
    db.commit()


if __name__ == '__main__':
    # 读取模型 识别菜 上传数据库

    # -------------init
    # loading  net
    inference_pb = "./frozen_inference_graph.pb"  # pb
    graph_txt = "./graph.pbtxt"                   # pbtxt
    net = load_md(graph_txt, inference_pb)
    # loading  mysql
    db = pymysql.connect('175.24.87.13', 'shuike', '123456', 'shuikedatabase', charset='utf8')
    cur = db.cursor()
    # ------------------------------------end
    # --------------一组图为一个菜单
    path = r'./menu'
    menu = os.listdir(path)     # 统计一组 菜的菜名
    print(menu)
    goods = []
    for url in menu:            # 识别菜   并统计
        good = read_img(path + '/' + url)
        for item in good:
            goods.append(item)
    print(goods)
    data = make_menu(goods)     # 生成订单
    menu_mysql(data)            # 上传订单
    # ------------------------------------end
    print('end')

