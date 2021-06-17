import sys
import time
#from cv2.dnn import DNN_BACKEND_INFERENCE_ENGINE, DNN_TARGET_CPU, DNN_BACKEND_OPENCV
import cv2
# import paddle
# import paddle.fluid as fluid
import paddlex as pdx
import numpy
import pymysql
import datetime
from alipay import AliPay

from PyQt5.QtCore import pyqtSignal, QThread, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication, QTableWidget

from source.ui2 import Ui_Form

from self_Alipay import alipay
from pay import pay


class My_ui_2(QWidget, Ui_Form):
    pb_qrode = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.heji = 0
        self.setupUi(self)

        # ---------------------------------------支付宝用到的参数
        self.APPID = '2016102400750258'
        self.private_key = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEAhfYwtdqJyoTcCOQsKn//swrTaHEa0HWueRZkyAdA1ItOPGhj7pzoKvxiDdix5vuREMwdJBs3bLNmi9ctMWjM4M3UxUMdNNU0M2vNlGgQthVRwNjASMAPFjk8z9H57XHoSaYKEJ7JpppdFG/noPuQybkdnX0zJFU1bXtM27RB64DYnV1wJKArSdofgV1fynyn2+7RjJq/guEYqS/o6/B/oWVVNblf8uDYEl/XeffDlXJCKKzvUG2XB4dkR796AWL7Zz8kFF7YiKyf/k4RB0MYTDVCsy0nvHgVS+GPV1SLDWddXIPbCq+4C422EL9CHs1DWBj/M+Eyo2x+IT5CyfH3hwIDAQABAoIBAFSmlm9D8pBz1isULEiK68Ry0daMqloSEzdXDEZONwxYHw8TFBrjMd5/72I6jWidjTSlFsELJcHdt64kQd2YEOb5ijtAxsLs+viHZbgi7nRxEmEfVppiKuZrMt9MG3eM5DEt5+xKurg5kRnqAN98OCkQfgNX6ypJYeKV6KJozMMIlTVueJBmyk9OYwtIs3Hy9C2THruT8XPsPPwUrxa9OaIJSn4Qu2190O/0GzcMBzpVQfDD0LZXQ/hxFDhRkJB9wDhHA1BHuQzKXscORuEl/Kwg6QtXJC3YTwCPVb/4YlXGfR0kF0ksRc7WdbwPY7sqVaTh7DzbqZY/hzn3Dgq3QgkCgYEAvo2eRdmY/LHNISVGNZvm2MCT6TbvBfKYhi7Ho8aYvCXFcJZHKyKTu6XeQcYTfp4EFRCuwIStfAvl0BCdwaPmoC9Gxk/itSyIDXdqsAs9iCJ5bY5FvIrwx/DS/Sht+nyKMRaMVyP3MNo+gaVM+Dz6Gi0RIC/8S2QNiNlB3mtC0BsCgYEAs/jD8ZI51gqcVMZatpGsn+glBTX/hEdcVEn4VpTmnNiYyX7hQAgugmEDpsgXfRywtRbrNu+nSledExwGzlpX8sLeu8tm5V+e2pu55PDwWuUp1wJr8yJE7Ls8ILR/Tggu1UAkelFuT7+1NeZsT+/LgMEa3deQ92HVNCOhRlWwJQUCgYEAlm3ESc47KRnQH1+GqqGVvv1ghxaX4XEfmaZqck9Amh+TW4s3ScU1LUkHSZNuJmHmRR7zZgYX0rqtxPCpKYoTcdeAnuPHzFEIYuEn9ywYelUE2UkconhpFt52IeZ90+XnTlNHnS9GYGmaOMzfE4VHx8xWHbvkBzxINwWUK1sv1osCgYAtA6O+4Fwm9TB048f8siMDPAVGcGMgqtilHHtI7KVhxasxetLMOT+ozKslJBb77BkmsjzS2M53AcL/7JqnMmGdDrC3OADcjjYlZ53vbXQwx/DXHnvxrDihHZPEemD9G37bR9fX4FY/DCw+9wtQUyILakFWC3zu40F4cRD9jqEoIQKBgFEifv+1k2wtMj4U913eTHxObX4atyOHn9LP+0bIqrNCD3+ZY9dBTmBaAXUcjmHB5YVCvzUSR0NgStrj9JdH2FUC4j2FF7nlwv6k/CxHVkkacilbTwK8MOalZQsgxZqMWpDD2jummrfc2Pa4Iswsr3wjXfczXehQlg8GAFJei//N
        -----END RSA PRIVATE KEY-----
        '''
        self.public_key = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjOTbJg1yZtSilND4oG/Hp70ydkSZ3nJ7sLmZKHI2E7d+9lbpzB+1ye6jEjYyHvesFCXVSCCLmW22OSqtnY6oqr+OjqgnIHtnrs0gwSb7xATcPMMAiU2GPcKs5JRak1I95q/unXeZi6HP9ypYpffIFouSkdPuVTkC2nfqJUO6bUEMoJerJeG2L+Mtp9itkDA1215NVq6gT6L2QTeeM7CVNkVNfedw/vne7G6KnxVh77//2dtppWfhLFkKs71BB0R2/NLn3jzulENKCnMmLjlKf/Y1cEXD/biPvKId+RR6lsYLvRF41NFqG2KL1AYYT7WtLABoaeB2kvjkwt/ifYR7wQIDAQAB
        -----END PUBLIC KEY-----
        '''
        # ----------------------------------------
        self.no = None
        self.data = None
        self.ID = 0
        self.menu = []
        self.init_table()

    # -------------初始化窗口
    def init_table(self):
        print('-----初始化-----')
        self.heji = 0
        self.ID = 0
        self.flags = False
        self.init_end = False
        self.menu = []
        self.frame = [0]
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
        self.label_2.setPixmap(QPixmap(""))
        self.label.setText('video cam')
        self.label_2.setText('支付二维码')
        # --------pb
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

    # 加载数据

    def paddlex_yuce(self, img):
        a = time.time()
        result = model.predict(img, eval_transforms)
        for i in result:
            print(i)
        b = (time.time() - a)
        print(b)
        pdx.det.visualize(img, result, threshold=0.7, save_dir='./')
        menu = []
        for item in result:
            if(item["score"] > 0.7):
                menu.append(item["category"])
        # 待修改
        # 在之后的menu变量中识别种类与数据库id对不上。
        return menu
        pass

    # -------------自定义函数

    def insert_table(self, data):
        menu = []  # 菜单 ---具体  真实数据 [[1, '', 16, 1], ]
        heji = 0  # 合计
        if len(data):
            for i, item in enumerate(data):
                sql2 = f"select * from good_list where good_name='{item}'"
                cur.execute(sql2)
                data2 = cur.fetchone()  # data2[id,name,price,size]
                good = [i + 1, str(data2[1]), int(data2[2]), 1, int(data2[2]) * 1]  # 临时缓存数据
                heji += good[4]
                menu.append(good)  # 添加真实数据
                # insert to tablewidget
                row = self.tableWidget.rowCount()

                if row == 1:
                    if self.tableWidget.item(row-1, 1) is not None:
                        if str(data2[1]) == str(self.tableWidget.item(row-1, 1).text()):
                            num = int(self.tableWidget.item(row-1, 3).text())
                            self.tableWidget.setItem(row-1, 3, QTableWidgetItem(str(num + 1)))
                            self.tableWidget.setItem(row-1, 4, QTableWidgetItem(str((num + 1) * int(data2[2]))))
                        else:
                            self.tableWidget.insertRow(row)
                            for j in range(len(good)):
                                self.tableWidget.setItem(row, j, QTableWidgetItem(str(good[j])))
                    else:
                        for j in range(len(good)):
                            self.tableWidget.setItem(row-1, j, QTableWidgetItem(str(good[j])))

                else:
                    k = 0
                    for i1 in range(row):
                        # print('00000', self.tableWidget.item(i1, 1).text())
                        if str(data2[1]) == str(self.tableWidget.item(i1, 1).text()):
                            num = int(self.tableWidget.item(i1, 3).text())
                            # print('num', num)
                            self.tableWidget.setItem(i1, 3, QTableWidgetItem(str(num + 1)))
                            self.tableWidget.setItem(i1, 4, QTableWidgetItem(str((num + 1) * int(data2[2]))))
                            k += 1
                            continue
                    if k == 0:
                        self.tableWidget.insertRow(row)
                        for j in range(len(good)):
                            self.tableWidget.setItem(row, j, QTableWidgetItem(str(good[j])))

            print('menu', menu)
            self.heji += heji
            # setting lineEdit
            self.lineEdit_3.setText(str(self.heji))
        pass

    def pb_qrode_func(self):
        print('-----生成二维码-----')
        # ----生成二维码
        frame = cv2.imread('./source/img/qr_test_ali.png')
        frame = cv2.resize(frame, (220, 220))
        # cv2.imshow('s', frame)
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.label_2.setPixmap(QPixmap(image))
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
        )  # pycryptodome
        i = 0
        while 1:
            time.sleep(1)
            result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)  # get 我们需要的 {'trade_status':}这个参数
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
    def pb_sure_img_click(self):
        if len(self.frame) == 3:

            menu = self.paddlex_yuce(self.frame[1])
            if len(menu) != 0:
                # print(menu)
                for item in menu:
                    self.menu.append(item)
                self.insert_table(menu)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)

    def pb_start_cam_click(self):
        print("-----开始 读取视频-----")
        self.init_end = False
        cap = cv2.VideoCapture(0)
        #frames_num = cap.get(7)
        # print(frames_num)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f'fps: {fps}')
        ret, frame = cap.read()
        while ret:
            frame = cv2.flip(frame, 1)
            self.frame.append(frame)
            if len(self.frame) == 4:
                self.frame.pop(0)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, dsize=(480, 320))  # 可以获取label 大小
            self.label.resize(QSize(480,320))
            # # mat-->qimage
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))

            ret, frame = cap.read()
            cv2.waitKey(int(1000 / fps) + 20)
            if not self.init_end:
                continue
            else:
                break
        else:
            print("-----结束 视频-----")
        pass

    def pb_end_order_click(self):
        if self.tableWidget.item(0, 1) is not None:
            print('-----生成订单号-----')
            now_time = datetime.datetime.now()
            now_time = now_time.strftime('%Y%m%d%H%M%S') + str(now_time)[-6:-1]
            print(now_time)
            self.lineEdit.setText(str(now_time))

            print('-----上传数据库-----')
            name = ''
            row = self.tableWidget.rowCount()
            col = self.tableWidget.colorCount()
            # print(self.tableWidget.item)

            for i in range(row):  # [3, 99.93, 34.12, 50.62, 499.18, 447.5]
                name += str(self.tableWidget.item(i, 0).text()) + 'x' + str(self.tableWidget.item(i, 3).text()) + ','
            name = name[:-1]
            print(name)
            no = self.lineEdit.text()
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 系统时间
            data = [str(no), name, now_time]
            sql0 = "select * from order_menu_list order by id desc limit 1;"
            cur.execute(sql0)
            row_last = cur.fetchall()
            # print(row_last)

            id = int(row_last[0][0])
            no = data[0]
            menu = data[1]
            time = data[2]
            self.heji = int(self.lineEdit_3.text())
            sql = f"insert into order_menu_list (id, no, menu, time, money) values (%s,%s,%s,%s,%s)"
            cur.execute(sql, (id + 1, no, menu, time, self.heji))
            db.commit()

            print('-----订单号对接支付宝 得到二维码地址-----')
            # no = str(uuid.uuid4())  # 生成订单号
            no = self.lineEdit.text()
            heji = int(self.lineEdit_3.text())
            subject = 'release'

            # 链接支付宝
            alipay1 = alipay(self.APPID, self.private_key, self.public_key)
            payer = pay(out_trade_no=no, total_amount=heji, subject=subject, timeout_express='5m')
            dict1 = alipay1.trade_pre_create(out_trade_no=payer.out_trade_no, total_amount=payer.total_amount,
                                             subject=payer.subject, timeout_express=payer.timeout_express)
            print(dict1)
            payer.get_qr_code(dict1["qr_code"])  # 获取二维码地址
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

    def pb_create_note_click(self):
        print('-----生成小票信息-----')
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

    def pb_clear_order_click(self):
        print('-----订单重置 按钮-----')
        self.init_end = True
        self.init_table()  # 初始化
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
        print(post)
        if post:  # 更新数据库的支付状态 信息
            status = '已支付'
        else:
            status = '未支付'
        sql = f"update order_menu_list set status='{status}' where no='{self.no}' "
        cur.execute(sql)
        self.post_status.emit(str(status))  # 发出信号
        db.commit()
        print("退出线程：", self.ID)

    pass


if __name__ == '__main__':
    # 说明
    # 该程序 ui实现功能  识别--> 生成订单 --> 结算

    # ------------------------------loading  net
    import matplotlib
    matplotlib.use('Agg')
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['CPU_NUM'] = '4'
    from paddlex.det import transforms

    print('-----加载模型-----')
    # paddlex_model_src = "model/aistudio/mask_rcnn_r50_fpn/epoch_10"
    #paddlex_model_src = "model/aistudio/mask_rcnn_r101_fpn/epoch_2"
    paddlex_model_src = "model/home/aistudio/output/face/faster_rcnn_r50_fpn/epoch_2"


    eval_transforms = transforms.Compose([
        transforms.Normalize(),
        transforms.ResizeByShort(short_size=800, max_size=1333),
        transforms.Padding(coarsest_stride=32)
    ])
    model = pdx.load_model(paddlex_model_src)

    print("___识别模型加载完成___")
    # -----------------------------链接数据库 全局化
    print('-----链接数据库------')
    db = pymysql.connect(host='localhost', user='root', password='root', database='testdb', charset='utf8')
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
        else:
            window.lineEdit_2.setStyleSheet('background: green;')
            # setting pushbutton


    sys.exit(app.exec_())  # app.exec_() 保持窗口刷新 sys.exit反馈错误类型
