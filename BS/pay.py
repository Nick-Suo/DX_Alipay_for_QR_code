from self_Alipay import *
import qrcode
import time

APPID = '2016102400750258'
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAjmdJluyFh7sccAAtVNs2oMI+DeUbJ880sm9vMy2EaRPaS/1YTyeqJ6MpRONEyOq9+c1hnNt+Wd3TuTP8ZjhSfXYQGGksyHoFfxreiwdRL5jR2oTtuPTZUOeuU0b7z79yH2bZ8zJYXTyjEyOPBXDFgyAvMBWU3AbMCNcezfN/dzAmt00rNIkMS+L4rEP4K1X9aRWhW/uLE5ujuT0Ae0oUypcw9vV+n3jQcFq7DBG7+VwOEFPA+EM3sLnssu7CYmFVuiAvxh10CVHPrbvxad5BWd6WAHAx7HmCvcrefuJmqEkOuoK1N5nCzzGEcL+ooGBE39fOqkZZ2OGG2Nr7mddGPQIDAQABAoIBADHN7A3t8RG0nlCJr1ETTjrRVLS1YVb+ADc8BA9JJxs9B0c2dxFQFRHB3egq+F6wwvrAGxiqJ7m0fJ00kl0J68fXZ++xsSj4jD2VHypOx9U2xIaBoUbj07GZJf4YQG+7TGWxKh8Fh6QsVfiWoinL9DhVJEvT8Hk3o1qgKjTrqbP8TIZ1T/slUPkUq07vJnx/co3K5hl9Zdq6fmkAnK4Lla5M2qcGi8YkrDpFZ94cVcaYt9UGqgBvTbMp+CfQdTapHbxGHgzpGeRKQZ8v/OB+0QyRyv9qDaDkgI6K/5HHTjJ7chaoFXMWwwfQ99xGv3G7wzsSBZIh+nDqfTs271219z0CgYEAyI1rXsLYeeZ1OH895PbBrGfxtml7JvZhj+zOla3TDUvRZpfD6h7gkHS1O7dKDoAOAt4wc6scdvsL/woMfKyE5qvEEkx6l19Gq5oqRK4NgGzZvnzxjUfhF/P0nK5Hp7eviuWyKp6s+kmYoui4uee25dOann04jGqKsEgi7ml2ENcCgYEAtcY8X2XkZMz9Y2PS6s/QscHO5BL5jrjCeBmYpmRXXml9dj/zy+oIyzPirbLAgi8xwnH2R7z7K63gSO77yu40N1SissSk5ZsnY0aUz/z3afYW+UCU9Tn3JVcgj9TWvrJN2eWcTcJNj0DDj4FGOqzJb/K0TrLWu9/1zU9Hc8/VOwsCgYA9tr7ulxjUUiWKMCWUupYYfpfz4Pujnreg+WcMykOi2MzkPBluhvflm/RVHu7sDV3CZisUvPfyaQhk/+udxdzTutGIK/6hbBEsJzGQltrSxSwwIPSX3CGZJFoGiN7F7pFXNZ2g3dku38zXfLOziWlPydDPqornMrXgzyHoqY1KWwKBgCsZZKkt7Jhl7lKJkbHxMkdjb52uThOkBSAa2ZHiSsDs/D10bmbUB9++XqnWr0Ru0jqLcNyTl25E3OAOIg98qU7RN35xl7OFNTKZwqEKFtO98LaKtIbshogI/4R676vpdQIMKiJZxrAHqBa3jSJOY7iycEQUrUuAj7RtbsCr75//AoGBAI9+CtMgjCM+CQ3ej4pS9bCMh/MHIeirVhIydZTEtTAd95rRyAErj02GXoOnuzSup0BZNK7Ss0ZOoC4SiCR2konyhrowk8wqJOEUR1YN08WaAAtO7Ovz0+W8ne75qbpSvs/KTLC+VJw80RSidI4YA15J5kYbvIIyLAe2wDMzCHlg
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
            ai = alipay.init_alipay_cfg()
            result = ai.api_alipay_trade_query(out_trade_no=out_trade_no)
            print(result)
            if not i % 30:
                print(str(i) + '..')
            else:
                print(i, end='..')
            if (result.get("trade_status", "") == "TRADE_SUCCESS" ) or (result.get("msg", "") == "Success"):
                print('订单已支付!')
                print('订单查询返回值：', result)
                return True
            _time += 2
        else:
            print('订单失效!')
            return False


if __name__ == '__main__':
    alipay = alipay(APPID, private_key, public_key)
    payer = pay(out_trade_no="4567893213", total_amount=5.04, subject="relive", timeout_express='1m')
    dict = alipay.trade_pre_create(out_trade_no=payer.out_trade_no, total_amount=payer.total_amount,
                                   subject=payer.subject, timeout_express=payer.timeout_express)
    #print(payer)
    payer.get_qr_code(dict["qr_code"])
    i = payer.query_order(alipay, payer.out_trade_no)
    print(i)
    print('0000')

