from self_Alipay import *
import qrcode
import time

APPID = '2016102400750258'
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAgEPlFsiHsjyzjT+RtjWBH6qCt2KK/54eazLCcBjZZ0rTziVhdKfpLEJZwZ/pSsoddLPlBLFA1RGFx9kJlYxfI12Emc9PbQjhQQlUJ/vb4fpVoDaKxt9Gt5n/621zyqncZBxVAaeDRKg38Pe1ReGrJN2nI6MF45wSEBL0nS2kdVvazYS7kggw2FWu1CvmQJx2hF123+rM8Tbil1UgY0nn4I9j8yTAORJU+cBDTOmdhJpTROcjmJbL7YNWZoeHtCUiBLsi8gDOwl0eRmwRofROjzBWEqI/9cavvCbTAZxsdfsvu7bDGKYpjYPk47Xat9CX+Ym4fA2Ra7EP0XITJQmtpQIDAQABAoIBACJbjXsL3iVlUydL1uk67cqgrwEWeWs9XKKUZzcFwP6FMbUvmCpabAA6Cbbu8dvhxgAjy/30yQwJ9I7y2Tlg738WptVYjcsELOpx6EQJl/2xQ8x1r7jTyCqYKtBSckjgNTPvzulxiJ0Ufl+iysDcUS6/3OyT15j/jmsV2MZdmocA3PQmIYCR1BgKEi1mzw9mlowigiKUuHSRO1BhVSgHdEby8iA6dq4a1NGpgstLqPFXXsPGEtvYr7GRUmNzjnUWjm98VvzNOQeS2dBN+0cZIOAHRLWc3MEP8G54wGzPMP1n2cbdS+nj1IDhNcC3QQ2FZLXLdwMN+6KBJhsbJLBVnAUCgYEA+BMr2zTQKT7eBl92RUgPkrUYclHyRHShcwwwDtm983qqDEIpKi5AG+CG5aIz5oa7ar7/FnuWxnbTE71VC38sUy7VefT6PwFDG4JPVFuFXd+08hETPocPoNs2iqwbWzfhtVRXEFQXE9liRCaYDmiCAb+7/xqjX4PDwAQ39/9OcjcCgYEAhFzimdTwNu/eJHIv1wpnnf3U26YQSbQpwizMtDAaEtdF/vAwuhjbXhZ2kCA9dkm9e6znLn6M+GEToLkQZF6MDowCd/0CCxkcNQfO7pQFrq6EdwYSKEvs1QIkDYN9OG6pkUnMiFROAseLj/DEs29WuHpYIbofKB0kf51gm4Mk4QMCgYEAxzneRrUrV3R9qnCP8yPkHdYCRA07m25vGo33KnYD7r3cQuv/UzjBk6HFtDWHqOMbMKcjBVNLyycybO/olMsVNdiu6LqtHlxNIJKOUxkNCk7WanD8G4MsMera6pM9hQxj39RT93EQ94flOwYjp66WegEZYc5q1hJj6pl4uVn4DhECgYBIakTzIoO1mq/vQqWXwbKExo2BCi6ZFD9QY5Au+K4bJrm9y4ztE5JYvHNrUKgvohJPqn3kewoHDZ1ebkFgmDWJ8+GZ4csPZVKAVOBKuKMPOZ1xPNoMP9W3h+9PkWOdzzVoLnb/ExiG/sMFIhWLkdthHFZBRYGsQZ1pUCG9kxdHHwKBgQDmf4M+fHCabeCBKkg5yJxGqrxc0UUQb1KqJioA+glgWTLY9li2DwdxJXTAmfKgVWbfwfn9vtxP2jOKpqoOWcH5L85RAGV3zknNmC8R300MCo/CffxeNX+xefKDfAe2efzIZLLLyyIY0jxltwwZGbB0ZX2DA3pTEuNJ4NOpUVBM0g==
-----END RSA PRIVATE KEY-----
'''
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjOTbJg1yZtSilND4oG/Hp70ydkSZ3nJ7sLmZKHI2E7d+9lbpzB+1ye6jEjYyHvesFCXVSCCLmW22OSqtnY6oqr+OjqgnIHtnrs0gwSb7xATcPMMAiU2GPcKs5JRak1I95q/unXeZi6HP9ypYpffIFouSkdPuVTkC2nfqJUO6bUEMoJerJeG2L+Mtp9itkDA1215NVq6gT6L2QTeeM7CVNkVNfedw/vne7G6KnxVh77//2dtppWfhLFkKs71BB0R2/NLn3jzulENKCnMmLjlKf/Y1cEXD/biPvKId+RR6lsYLvRF41NFqG2KL1AYYT7WtLABoaeB2kvjkwt/ifYR7wQIDAQAB
-----END PUBLIC KEY-----
'''


class pay:
    def __init__(self, out_trade_no, total_amount, subject, timeout_express):
        self.out_trade_no = out_trade_no    # 订单
        self.total_amount = total_amount    # 商品
        self.subject = subject              # 价格
        self.timeout_express = timeout_express  # 订单超时 时间

    def get_qr_code(self, code_url):
        '''
        生成二维码
        :return None
        '''

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1
        )
        qr.add_data(code_url)  # 二维码所含信息
        img = qr.make_image()  # 生成二维码图片
        img.save(r'./source/img/qr_test_ali.png')
        print('二维码已生成！')

    def query_order(self, alipay, out_trade_no):
        '''
        :param out_trade_no: 商户订单号
        :return: Nonem
        '''
        _time = 0
        for i in range(1, 61):
            time.sleep(1)
            result = alipay.init_alipay_cfg(self).api_alipay_trade_query(out_trade_no=out_trade_no)
            print(result)
            if not i % 30:
                print(str(i) + '..')
            else:
                print(i, end='..')
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                print('订单已支付!')
                print('订单查询返回值：', result)
                return True
            _time += 2
        else:
            print('订单失效!')
            return False


if __name__ == '__main__':
    alipay = alipay(APPID, private_key, public_key)
    payer = pay(out_trade_no="aa-a", total_amount=5.04, subject="relive", timeout_express='1m')
    dict = alipay.trade_pre_create(out_trade_no=payer.out_trade_no, total_amount=payer.total_amount,
                                   subject=payer.subject, timeout_express=payer.timeout_express)
    print(dict)
    payer.get_qr_code(dict['qr_code'])
    i = payer.query_order(alipay, payer.out_trade_no)
    print(i)
    print('0000')

