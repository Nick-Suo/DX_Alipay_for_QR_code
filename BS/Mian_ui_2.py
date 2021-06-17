import sys
import time
from cv2.dnn import DNN_BACKEND_INFERENCE_ENGINE, DNN_TARGET_CPU, DNN_BACKEND_OPENCV
import cv2
import paddle
import paddle.fluid as fluid
import numpy
import pymysql
from alipay import AliPay

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication, QTableWidget

from source.main_ui_just_pay import Ui_Form

from self_Alipay import alipay
from pay import pay


class My_ui_2(QWidget, Ui_Form):
    pb_qrode = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.heji = 0
        self.setupUi(self)

        # ---------------------------------------支付宝用到的参数
        self.APP_ID = '2016102400750258'
        self.private_key = '''-----BEGIN RSA PRIVATE KEY-----MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCZy6TMmt+z3HJWliaWR93SGVU8DBfCZvf0X7WBmNnLVkIP69rmccPoyvnSdwtFMdzYHv5zSTRUSl5YsdXqrzncV4tA2ZYgowYY83SoetiPQQ7y5OyOCb1/UePokbvCqcqhpJ6AWYgCTIhYRw35pGCbaORtGGQeGIksb/SqBhtDYNOKpbZd1lGlw5n8MOdeJngf+5m33oBWNfJA6XgyeJ57H4wDdM+5TLqC4D4jEyZSpzRacOCaE/VJuf3xnIbOndoW7PpbFBgceivUHMUNdOBghpmB7VaYMiQs+Rdw8CcG3vD6N10vRefRsAvC8R6dGAOOjr8LZvlDV3WSQUbLlzA9AgMBAAECggEANfIkoFBC34gX4x9P8a7LtAKGz0U+oEYV+3YG6KqA2r4q9gK5CdQl7+Yisxxmq6LN4FEe17l5zYc4iMv4SRWlqhBbHCg2bMRCQ0ZCSUat57HeWHzMLRZljd9fnhhgT+vW09Q2dLby6juGJ9DkqghqipjEZzADDjt1Ak1S+MCjl4I0me8G5f5vrhp7GjuWW03clWZjDoeynGJnysZ7i0ojJJ38x3MlcofvB1r8XvmoFNmGYczZ+ZpLwzhgWoM2Mbh9tZ19YNJABz0qoR1dVWUEch5FliY5Z8at8REUB8lzSUl9IyrYWcK4Nqv1biu9fQWryiIcr4Sjqd3UHAqJ9U/R0QKBgQD3UiF4HO8cmL2L/Pw6KD1sS3q/mr3TuOk0+vUEtpjh3YK+UwI5GgNQGXaaQwRozZEuF6keKPSKSeyiULkOf9Czm0QUnCUClZsahi7Vn7WXRtYL3D4Vvp24ye83NH6qv27d1UyDSZeD56ZSoJZMkjoImy+YgVHDs6yZNkilqL2RUwKBgQCfMU3u/yPQdlk069fiAjxYuRM4wvuC1JGamqdzmQg+4QqAkN21hItekhq1oHgk7OcJvi2uUyQUedqXr/6AOfgNsU0DKhGY1DApx1vvIXXEDdrf0/gLdndbZeZ+t67KKGGdfl0osMWqUwdRDaxAo58HeFE4m0MwUk/3jjA+bRY2LwKBgQCsiUeAG+9T69qQBnWPvPLc0etYMAOt6JoIs+qq1xfguj+ztwUeAN++yYTMKWSyGHbnyOnaeIfg0aGbuuTfEJvwMKlWF3haTTRfVKznqvtsBabdr1BAqzIs7/NKd/zF8bbOWzd9f6GMC9ckXZN856ZEyr5xjgYUmQwX9p7HsuhMsQKBgFgsqwoR7/hrVQXnC/B3ZI2QFYF/Hmhc7TlBKDbzMIoDhBmqI+OCwt9i9cBcXa+2OFJBMHQ6QOXGiLk0FjdX5HlRF2MFTjHkdbjuX5GYau5o7i7D7cQLnhjV3FGb1AjNTSQ69cawAwxQaOEQPbSf7Fnq3rIH7bM6JGjuLPKm4YKpAoGBAILvY6i+cOJw3VlJjFcwECHzWWkOa69OQh0YNl2q3RUpDIW+2rVWOOaN8wvvbKlL7x4hY2Vk6xbuYDF88dTZQSN/f4USCYj2bIa9dFkSS2h3l1UAI2TbC6n+fT3UKfBW2C1R1zwd70XEmznwyEbiWRZeVC7nwfe9dzU+Wn1p5/tB-----END RSA PRIVATE KEY-----
                '''
        self.public_key = '''-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmcukzJrfs9xyVpYmlkfd0hlVPAwXwmb39F+1gZjZy1ZCD+va5nHD6Mr50ncLRTHc2B7+c0k0VEpeWLHV6q853FeLQNmWIKMGGPN0qHrYj0EO8uTsjgm9f1Hj6JG7wqnKoaSegFmIAkyIWEcN+aRgm2jkbRhkHhiJLG/0qgYbQ2DTiqW2XdZRpcOZ/DDnXiZ4H/uZt96AVjXyQOl4Mnieex+MA3TPuUy6guA+IxMmUqc0WnDgmhP1Sbn98ZyGzp3aFuz6WxQYHHor1BzFDXTgYIaZge1WmDIkLPkXcPAnBt7w+jddL0Xn0bALwvEenRgDjo6/C2b5Q1d1kkFGy5cwPQIDAQAB-----END PUBLIC KEY-----
                '''
        # ----------------------------------------
        self.no = None
        self.data = None
        self.ID = 0
        self.init_table()

    # -------------初始化窗口
    def init_table(self):
        print('-----初始化-----')
        self.heji = 0
        self.ID = 0
        # ----------tablewidget
        self.tableWidget.clear()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        col_list = ['id', '食物', '单价(元)', '个数', '价格(元)']
        self.tableWidget.setHorizontalHeaderLabels(col_list)
        print(col_list)
        # ---------lineEdit
        self.lineEdit.clear()

        self.lineEdit_2.clear()
        self.lineEdit_2.setStyleSheet('')

        self.lineEdit_3.clear()
        # --------label
        self.label.setPixmap(QPixmap(""))
        self.label.setText('支付二维码')
        # --------pb
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        # net
        # inference_pb = "./model/frozen_inference_graph.pb"  # pb
        # graph_txt = "./model/graph.pbtxt"  # pbtxt
        # net = self.load_md(graph_txt, inference_pb)
        # url = './model/menu/10592.jpg'
        # img = cv2.imread(url)
        #
        # im_tensor = cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False)
        # net.setInput(im_tensor)
        # cvOut = net.forward()
        # for detect in cvOut[0, 0, :, :]:
        #     detect = detect.tolist()  # numpy  ->  list
        #     score = detect[2]
        #     h, w = img.shape[:2]
        #     detect[1] = int(detect[1])
        #     detect[2] = float(f"{detect[2] * 100 :.2f}")  # 统一概率格式 00.0
        #     detect[3] = float(f"{detect[3] * w :.2f}")
        #     detect[4] = float(f"{detect[4] * h :.2f}")
        #     detect[5] = float(f"{detect[5] * w :.2f}")
        #     detect[6] = float(f"{detect[6] * h :.2f}")
        #     if score > 0.91:
        #         print(detect)
        # cv2.imshow(url, img)
        # cv2.waitKey(0)

    def load_md(self, graph_txt, inference_pb):
        # inference_pb = "frozen_inference_graph.pb"  # pb
        # graph_txt = "graph.pbtxt"                   # txt
        net = cv2.dnn.readNetFromTensorflow(inference_pb,
                                           graph_txt)  # 旧版 需要手动在cv2文件夹里更换cv2.cp37-win_amd64.pyd      10fps
        # net = cv.dnn.readNetFromModelOptimizer(graph_xml, inference_bin)  # openvino 需要手动在cv2文件夹里更换cv2.pyd  60fps
        net.setPreferableBackend(DNN_BACKEND_INFERENCE_ENGINE)  # openvino加速    # 默认设置 可以不添加
        net.setPreferableTarget(DNN_TARGET_CPU)  # 。。
        return net

    # 加载数据
    def load_img(path):
        #img = paddle.dataset.image.load_and_transform(path, 100, 100, False).astype("float32")
        img = paddle.dataset.image.simple_transform(path, 100, 100, False).astype("float32")
        img = img / 255.0
        return img

    def paddle_yuce(self, model_src, img):
        # 定义执行器
        place = fluid.CPUPlace()
        infer_exe = fluid.Executor(place)
        model_save_dir = model_src  # 模型保存路径

        infer_imgs = []  # 存放要预测图像数据
        infer_imgs.append(self.load_img(img))  # 加载图片，并且将图片数据添加到待预测列表
        infer_imgs = numpy.array(infer_imgs)  # 转换成数组

        # 加载模型
        infer_program, feed_target_names, fetch_targets = fluid.io.load_inference_model(model_save_dir, infer_exe)

        # 执行预测
        results = infer_exe.run(infer_program,  # 执行预测program
                                feed={feed_target_names[0]: infer_imgs},  # 传入待预测图像数据
                                fetch_list=fetch_targets)  # 返回结果
        # 预测
        name_list = ["kele", "lvcha", "micha", "nfsq", "binglu"]    # 类
        label = []
        result = numpy.argmax(results[0])  # 取出预测结果中概率最大的元素索引值

        print(name_list[result])

        return name_list[result]

    # -------------自定义函数

    def pb_qrode_func(self):
        print('-----生成二维码-----')
        # ----生成二维码
        frame = cv2.imread('./source/img/qr_test_ali.png')
        frame = cv2.resize(frame, (220, 220))
        # cv2.imshow('s', frame)
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap(image))
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()

    def post_alipay_func(self, out_trade_no):
        print('-----刷新post-----')
        # 刷新 post
        alipay = AliPay(
            appid=self.APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=self.private_key,
            alipay_public_key_string=self.public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False ,若开启则使用沙盒环境的支付宝公钥
        )   # pycryptodome
        i = 0
        while 1:
            time.sleep(1)
            result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)   # get 我们需要的 {'trade_status':}这个参数
            print(i, end='..')
            if i < 61:
                i += 1
                if result.get("trade_status", "") == "TRADE_SUCCESS":
                    print(result)
                    print('订单已支付!')
                    # print('订单查询返回值：', result)
                    return True
            else:
                print(result)
                print('订单未支付!')
                return False
        pass

    # -------------自定义signal

    def tx_dingdanhao_change(self, order_number):
        print('-----信号-订单号发生改变-----')
        # 获取订单中的信息  并显示在对应控件上
        self.no = order_number  # 订单号
        # print(self.no)
        if len(order_number) > 0:
            self.init_table()
            self.lineEdit.setText(str(self.no))
            try:
                sql = f"select * from order_menu_list where no='{order_number}'"
                cur.execute(sql)
                data = cur.fetchone()   # 订单内的信息
                print('-----搜索对应订单-----')
                print(data)
                self.data = data
            except:
                self.data = None
                print("no find")
                pass
            if self.data:  # data = (1, '001', '3x1,4x2,5x3', datetime.datetime(2020, 5, 7, 17, 43, 40), 163, '已支付')
                print('-----提取订单内信息-----')
                no = self.data[1]  # 单号
                time = self.data[3]  # 时间
                money = self.data[4]  # 总价
                status = self.data[5]  # 支付状态

                menu = []  # 菜单 ---具体的菜  真实数据 [[1, '独面筋', 16, 1], ]
                menu_c = self.data[2].split(',')  # 菜单 ---具体的菜  测试数据
                print('menu_c', menu_c)
                heji = 0  # 合计
                for i, item in enumerate(menu_c):
                    y = item.split('x')
                    # 查询 这个菜 单价
                    sql2 = f"select * from good_list where id='{y[0]}'"
                    cur.execute(sql2)
                    data2 = cur.fetchone()  # data2[id,name,price,size]
                    # -----
                    good = [i + 1, str(data2[1]), int(data2[2]), int(y[1]), int(data2[2]) * int(y[1])]  # 临时缓存数据
                    heji += good[4]
                    menu.append(good)  # 添加真实数据
                    # insert to tablewidget
                    if i != 0:
                        self.tableWidget.insertRow(i)
                    for j in range(len(good)):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(good[j])))
                print('menu', menu)
                self.heji = heji
                # setting lineEdit
                self.lineEdit_3.setText(str(heji))
                # setting pushbutton
                self.pushButton.setEnabled(True)
                self.pushButton_3.setEnabled(True)
                # update mysql
                print('-----更新数据库 账单money信息-----')
                sql3 = f"update order_menu_list set money='{heji}' where no='{no}'"
                cur.execute(sql3)
                db.commit()
            else:
                self.pushButton.setEnabled(False)
        else:
            print('-----空白订单号 初始化-----')
            self.init_table()

    def pb_end_click(self):
        print('-----订单号对接支付宝 得到二维码地址-----')
        # no = str(uuid.uuid4())  # 生成订单号
        no = self.no
        heji = int(self.lineEdit_3.text())
        subject = 'release'

        # 链接支付宝
        alipay1 = alipay(self.APPID, self.private_key, self.public_key)
        payer = pay(out_trade_no=no, total_amount=heji, subject=subject, timeout_express='5m')
        dict1 = alipay1.trade_pre_create(out_trade_no=payer.out_trade_no, total_amount=payer.total_amount,
                                         subject=payer.subject, timeout_express=payer.timeout_express)
        print(dict1)
        payer.get_qr_code(dict1['qr_code'])  # 获取二维码地址
        # -------线程 接收支付信息
        print('-----开始线程-----')
        thread1 = myThread(no=payer.out_trade_no, ID=1)
        thread1.start()
        thread1.post_status.connect(xxx)
        # --------------------
        # -------加载二维码
        print('-----加载二维码-----')
        self.pb_qrode.emit()
        # ---------------------
        pass

    def pb_xiaopiao_click(self):
        print('------生成小票信息-----')
        xiaopiao = []
        row = self.tableWidget.rowCount()
        col = self.tableWidget.colorCount()
        for i in range(row):
            x = []
            for j in range(col):
                try:
                    data = self.tableWidget.item(i, j).text()
                    x.append(data)
                except:
                    continue
            xiaopiao.append(x)
        print('xiaopiao', xiaopiao)
        pass

    def pb_remove_click(self):
        print('-----订单重置 按钮-----')
        self.init_table()  # 初始化
        pass

    def pb_insert_click(self):
        print('-----insert-----')
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        pass

    def pb_delete_click(self):
        print('-----delete-----')
        row_index = self.tableWidget.currentRow()
        self.tableWidget.removeRow(row_index)
        pass


class myThread(QThread):
    post_status = pyqtSignal(str)

    def __init__(self, no, ID):
        super(myThread, self).__init__()
        self.my_ui = My_ui_2()
        self.no = no  # 订单号
        self.ID = ID

    def run(self):
        print("开始线程：", self.ID)
        post = self.my_ui.post_alipay_func(self.no)
        print('-----更新 支付状态status信息-----')
        if post:  # 更新数据库的支付状态 信息
            status = '已支付'
            sql = f"update order_menu_list set status='{status}' where no='{self.no}' "
            cur.execute(sql)
            self.post_status.emit(str(status))  # 发出信号
        else:
            status = '未支付'
            sql = f"update order_menu_list set status='{status}' where no='{self.no}' "
            cur.execute(sql)
            self.post_status.emit(str(status))
        db.commit()
        print("退出线程：", self.ID)

    pass


if __name__ == '__main__':
    # 说明
    # # 环境
    # #     主要库 py=3.7 opencv=4.2 PyQt5=5.14.1 qrcode pymysql python-alipay-sdk pycryptodome
    # #     其他的库 具体看 Main_ui_2.py pay.py self_Alipay.py 中导入的库，比较多

    # 该程序 ui实现功能  输入数据库订单 --> 结算 --> 输入

    # -----------------------------先链接数据库 全局化
    print('-----链接数据库------')
    #db = pymysql.connect('175.24.87.13', 'shuike', '123456', 'shuikedatabase', charset='utf8')
    db = pymysql.connect('localhost', 'root', 'root', 'testdb', charset='utf8')
    cur = db.cursor()

    # -----------------------------展示ui
    print('-----展示ui-----')
    app = QApplication(sys.argv)  # sys.argv 反馈窗口输入
    window = My_ui_2()
    window.show()  # 窗口显示
    window.pb_qrode.connect(window.pb_qrode_func)

    def xxx(status):  # 这是class myThread 线程 信号接收的函数
        print('-----xxx槽函数启动-----')
        window.lineEdit_2.setText(status)
        if status == '未支付':
            window.lineEdit_2.setStyleSheet('background: red;')
            # setting pushbutton
            window.pushButton_2.setEnabled(False)
        else:
            window.lineEdit_2.setStyleSheet('background: green;')
            # setting pushbutton
            window.pushButton_2.setEnabled(True)

    sys.exit(app.exec_())  # app.exec_() 保持窗口刷新 sys.exit反馈错误类型
