# -*- coding: UTF-8 -*-
import base64
import collections
import copy
import json
from datetime import datetime
from urllib import request, parse
import rsa
from alipay import AliPay

APP_ID = '2016102400750258'
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAgEPlFsiHsjyzjT+RtjWBH6qCt2KK/54eazLCcBjZZ0rTziVhdKfpLEJZwZ/pSsoddLPlBLFA1RGFx9kJlYxfI12Emc9PbQjhQQlUJ/vb4fpVoDaKxt9Gt5n/621zyqncZBxVAaeDRKg38Pe1ReGrJN2nI6MF45wSEBL0nS2kdVvazYS7kggw2FWu1CvmQJx2hF123+rM8Tbil1UgY0nn4I9j8yTAORJU+cBDTOmdhJpTROcjmJbL7YNWZoeHtCUiBLsi8gDOwl0eRmwRofROjzBWEqI/9cavvCbTAZxsdfsvu7bDGKYpjYPk47Xat9CX+Ym4fA2Ra7EP0XITJQmtpQIDAQABAoIBACJbjXsL3iVlUydL1uk67cqgrwEWeWs9XKKUZzcFwP6FMbUvmCpabAA6Cbbu8dvhxgAjy/30yQwJ9I7y2Tlg738WptVYjcsELOpx6EQJl/2xQ8x1r7jTyCqYKtBSckjgNTPvzulxiJ0Ufl+iysDcUS6/3OyT15j/jmsV2MZdmocA3PQmIYCR1BgKEi1mzw9mlowigiKUuHSRO1BhVSgHdEby8iA6dq4a1NGpgstLqPFXXsPGEtvYr7GRUmNzjnUWjm98VvzNOQeS2dBN+0cZIOAHRLWc3MEP8G54wGzPMP1n2cbdS+nj1IDhNcC3QQ2FZLXLdwMN+6KBJhsbJLBVnAUCgYEA+BMr2zTQKT7eBl92RUgPkrUYclHyRHShcwwwDtm983qqDEIpKi5AG+CG5aIz5oa7ar7/FnuWxnbTE71VC38sUy7VefT6PwFDG4JPVFuFXd+08hETPocPoNs2iqwbWzfhtVRXEFQXE9liRCaYDmiCAb+7/xqjX4PDwAQ39/9OcjcCgYEAhFzimdTwNu/eJHIv1wpnnf3U26YQSbQpwizMtDAaEtdF/vAwuhjbXhZ2kCA9dkm9e6znLn6M+GEToLkQZF6MDowCd/0CCxkcNQfO7pQFrq6EdwYSKEvs1QIkDYN9OG6pkUnMiFROAseLj/DEs29WuHpYIbofKB0kf51gm4Mk4QMCgYEAxzneRrUrV3R9qnCP8yPkHdYCRA07m25vGo33KnYD7r3cQuv/UzjBk6HFtDWHqOMbMKcjBVNLyycybO/olMsVNdiu6LqtHlxNIJKOUxkNCk7WanD8G4MsMera6pM9hQxj39RT93EQ94flOwYjp66WegEZYc5q1hJj6pl4uVn4DhECgYBIakTzIoO1mq/vQqWXwbKExo2BCi6ZFD9QY5Au+K4bJrm9y4ztE5JYvHNrUKgvohJPqn3kewoHDZ1ebkFgmDWJ8+GZ4csPZVKAVOBKuKMPOZ1xPNoMP9W3h+9PkWOdzzVoLnb/ExiG/sMFIhWLkdthHFZBRYGsQZ1pUCG9kxdHHwKBgQDmf4M+fHCabeCBKkg5yJxGqrxc0UUQb1KqJioA+glgWTLY9li2DwdxJXTAmfKgVWbfwfn9vtxP2jOKpqoOWcH5L85RAGV3zknNmC8R300MCo/CffxeNX+xefKDfAe2efzIZLLLyyIY0jxltwwZGbB0ZX2DA3pTEuNJ4NOpUVBM0g==
-----END RSA PRIVATE KEY-----
'''
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjOTbJg1yZtSilND4oG/Hp70ydkSZ3nJ7sLmZKHI2E7d+9lbpzB+1ye6jEjYyHvesFCXVSCCLmW22OSqtnY6oqr+OjqgnIHtnrs0gwSb7xATcPMMAiU2GPcKs5JRak1I95q/unXeZi6HP9ypYpffIFouSkdPuVTkC2nfqJUO6bUEMoJerJeG2L+Mtp9itkDA1215NVq6gT6L2QTeeM7CVNkVNfedw/vne7G6KnxVh77//2dtppWfhLFkKs71BB0R2/NLn3jzulENKCnMmLjlKf/Y1cEXD/biPvKId+RR6lsYLvRF41NFqG2KL1AYYT7WtLABoaeB2kvjkwt/ifYR7wQIDAQAB
-----END PUBLIC KEY-----
'''


class alipay:
    def __init__(self, app_id, private_key, public_key, notify_url=None, charset='gbk', sign_type='RSA2',
                 version='1.0', DEBUG=True):
        self.requesturl = 'https://openapi.alipay.com/gateway.do' if DEBUG is False else "https://openapi.alipaydev.com/gateway.do"
        self.private_key = private_key
        self.public_key = public_key
        self.params = dict(app_id=app_id, charset=charset, sign_type=sign_type, version=version,
                           biz_content={}, timestamp='', notify_url=notify_url)

    def _sort(self, params):
        # print(collections.OrderedDict(sorted(dict(params).items(), key=lambda x: x[0])))
        return collections.OrderedDict(sorted(dict(params).items(), key=lambda x: x[0]))

    @staticmethod
    def make_goods_etail(goods_detail=None, alipay_goods_id=None, goods_name=None, quantity=None, price=None,
                         goods_category=None, body=None, show_url=None):
        params = dict(goods_detail=goods_detail, alipay_goods_id=alipay_goods_id, goods_name=goods_name,
                      quantity=quantity, price=price, goods_category=goods_category, body=body, show_url=show_url)
        return dict(filter(lambda x: x[1] is not None, params.items()))

    def _make_sign(self, params, **kwargs):
        private_key = rsa.PrivateKey.load_pkcs1(kwargs.get('private_key', None) or self.private_key)
        sign = base64.b64encode(rsa.sign(params.encode(), private_key, "SHA-256")).decode('gbk')
        return sign

    def _check_sign(self, message, sign, **kwargs):
        message = self._sort(message)
        data = '{'
        for key, value in message.items():
            data += '"{}":"{}",'.format(key, value)
        data = data[:-1] + '}'
        sign = base64.b64decode(sign)
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(kwargs.get('public_key', None) or self.public_key)
        try:
            rsa.verify(data.encode(), sign, public_key)
            return True
        except Exception:
            return False

    def _make_request(self, params, biz_content, **kwargs):
        buf = ''
        params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['biz_content'] = json.dumps(self._sort(biz_content))
        for key, value in kwargs.items():
            params[key] = value
        params = self._sort(params)
        for key in params:
            buf += '{}={}&'.format(key, params[key])
        params['sign'] = self._make_sign(buf[:-1], **kwargs)
        # print(params)
        # 发射http请求取回数据
        data = request.urlopen(self.requesturl, data=parse.urlencode(params).encode('gbk')).read().decode('gbk')
        # print(parse.urlencode(params).encode('gbk'))
        return data

    def parse_response(self, params, **kwargs):
        sign = params['sign']
        if self._check_sign(dict(filter(lambda x: 'sign' not in x[0], params.items())), sign, **kwargs):
            return True
        else:
            return False

    def trade_pre_create(self, out_trade_no, total_amount, subject, seller_id=None, discountable_amount=None,
                         undiscountable_amount=None, buyer_logon_id=None, body=None, goods_detail=None,
                         operator_id=None, store_id=None, terminal_id=None, timeout_express=None, alipay_store_id=None,
                         royalty_info=None, extend_params=None, **kwargs):
        """
        :param out_trade_no:    商户订单号,64个字符以内、只能包含字母、数字、下划线；需保证在商户端不重复.
        :param total_amount:    订单总金额，单位为元，精确到小数点后两位.
        :param subject:         订单标题.
        :param seller_id:       卖家支付宝用户ID。 如果该值为空，则默认为商户签约账号对应的支付宝用户ID.
        :param discountable_amount:可打折金额. 参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
        :param undiscountable_amount:不可打折金额. 不参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
        :param buyer_logon_id:      买家支付宝账号
        :param body:                对交易或商品的描述
        :param goods_detail:        订单包含的商品列表信息.使用make_goods_etail生成. 其它说明详见：“商品明细说明”
        :param operator_id:         商户操作员编号
        :param store_id:            商户门店编号
        :param terminal_id:         商户机具终端编号
        :param timeout_express:     该笔订单允许的最晚付款时间，逾期将关闭交易。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天
        :param alipay_store_id:     支付宝店铺的门店ID
        :param royalty_info:        描述分账信息   暂时无效
        :param extend_params:       业务扩展参数	暂时无效
        :param kwargs:              公共参数可在此处暂时覆盖
        :return:
        """
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.precreate'
        total_amount = round(int(total_amount), 2)
        if discountable_amount:
            discountable_amount = round(int(discountable_amount), 2)
        if undiscountable_amount:
            undiscountable_amount = round(int(undiscountable_amount), 2)
        if discountable_amount:
            if undiscountable_amount is not None:
                if discountable_amount + undiscountable_amount != total_amount:
                    return '传入打折金额错误'
        biz_content = dict(out_trade_no=out_trade_no[:64], total_amount=total_amount, seller_id=seller_id,
                           subject=subject,
                           discountable_amount=discountable_amount, undiscountable_amount=undiscountable_amount,
                           buyer_logon_id=buyer_logon_id, body=body, goods_detail=goods_detail, operator_id=operator_id,
                           store_id=store_id, terminal_id=terminal_id, timeout_express=timeout_express,
                           alipay_store_id=alipay_store_id, royalty_info=royalty_info, extend_params=extend_params)
        # print(biz_content)
        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)
        # print(resp)
        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_precreate_response']
        if self._check_sign(check['alipay_trade_precreate_response'], check['sign']):
            return resp
        return False

    def trade_refund(self, refund_amount, out_trade_no=None, trade_no=None,
                     refund_reason=None, out_request_no=None, operator_id=None, store_id=None,
                     terminal_id=None, **kwargs):
        """

        :param refund_amount:   需要退款的金额，该金额不能大于订单金额,单位为元，支持两位小数
        :param out_trade_no:    商户订单号，不可与支付宝交易号同时为空
        :param trade_no:        支付宝交易号，和商户订单号不能同时为空
        :param refund_reason:   退款的原因说明
        :param out_request_no:  标识一次退款请求，同一笔交易多次退款需要保证唯一，如需部分退款，则此参数必传。
        :param operator_id:     商户的操作员编号
        :param store_id:        商户的门店编号
        :param terminal_id:     商户的终端编号
        :param kwargs:          公共参数可在此处临时覆盖
        :return:
        """
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.refund'
        refund_amount = round(float(refund_amount), 2)

        biz_content = dict(refund_amount=refund_amount, out_trade_no=out_trade_no, trade_no=trade_no,
                           refund_reason=refund_reason, out_request_no=out_request_no, operator_id=operator_id,
                           store_id=store_id, terminal_id=terminal_id)
        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)
        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_refund_response']
        if self._check_sign(check['alipay_trade_refund_response'], check['sign']):
            return int(resp['code']) == 10000
        return False

    def trade_query(self, out_trade_no, trade_no=None, **kwargs):
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.query'

        biz_content = dict(out_trade_no=out_trade_no, trade_no=trade_no)
        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)
        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_query_response']
        if self._check_sign(check['alipay_trade_query_response'], check['sign']) and resp['code'] == 10000:
            return resp
        return False

    def init_alipay_cfg(self):
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=private_key,
            alipay_public_key_string=public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False ,若开启则使用沙盒环境的支付宝公钥
        )
        return alipay
