#coding:utf8

from xml.etree.ElementTree import Element, tostring
import requests
import string
import random
import hashlib
from time import localtime, strftime
import json
import xmltodict


class MchPay:

    __request_data = {}

    def __init__(self, appid, mchid, key, cert_path, key_path):
        """
        初始化对象，传入appid和mchid
        :param appid: appid
        :param mchid: 微信支付商户id
        :param key: 后台设置的key，具体解释见https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=4_3
        :param cert_path: pem证书路径
        :param key_path: pem私钥路径
        """
        self.__request_data['mch_appid'] = appid          # appid
        self.__request_data['mchid'] = mchid              # 商户id
        self.__request_data['key'] = key                  # API key
        self.__request_data['cert_path'] = cert_path      # 证书路径
        self.__request_data['key_path'] = key_path        # 私钥路径

    def setup(self, openid, amount, desc, trade_sn='', ip=''):
        """
        设置一次付款
        :param openid: 目标用户openid
        :param amount: 付款金额，单位为分
        :param desc: 付款描述
        :param trade_sn: 商户订单号。在发起一次新交易时不需要传入，系统会自动生成一个。如果需要重试之前的交易，则需要传入。
        :param ip: IP地址，如果没有传入则自动获取
        :return:
        """
        self.__request_data['nonce_str'] = self.__generate_nonce_str(30)          # 随机字符串
        if not trade_sn:
            self.__request_data['partner_trade_no'] = self.__generate_trade_sn()  # 商户订单号
        else:
            self.__request_data['partner_trade_no'] = trade_sn
        self.__request_data['openid'] = openid            # 用户openid
        self.__request_data['check_name'] = 'NO_CHECK'    # 校验用户名
        self.__request_data['amount'] = amount            # 付款金额，单位为分
        self.__request_data['desc'] = desc                # 描述
        if not ip:
            self.__request_data['spbill_create_ip'] = self.__get_current_ip()      # IP地址
        else:
            self.__request_data['spbill_create_ip'] = ip
        self.__request_data['sign'] = self.__sign(self.__request_data['key'])      # 签名
        return True

    def send(self):
        """
        发送付款请求
        :return: 返回一个包含三个元素的数组，分别为：结果（'success'/'fail），错误码，错误信息
        """
        d = self.__dict_to_xml('xml', self.__request_data)
        d = tostring(d)
        r = requests.post(
            'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers',
            data=d,
            cert=(self.__request_data['cert_path'], self.__request_data['key_path'])
        )
        ret = xmltodict.parse(r.text)['xml']
        result = [ret['result_code'], ret['err_code'], ret['return_msg']]
        return result

    def __get_current_ip(self):
        """
        获得当前的公网IP
        :return:
        """
        rst = requests.get('https://ipapi.co/json/').text
        ip = json.loads(rst)['ip']
        return ip

    def __sign(self, key):
        """
        签名，具体签名算法见https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=4_3
        :param key:
        :return:
        """
        raw_string = 'amount={}&check_name={}&desc={}&mch_appid={}&mchid={}&nonce_str={}&openid={}&partner_trade_no={}&spbill_create_ip={}&key={}'.format(
            str(self.__request_data['amount']),
            self.__request_data['check_name'],
            self.__request_data['desc'],
            self.__request_data['mch_appid'],
            self.__request_data['mchid'],
            self.__request_data['nonce_str'],
            self.__request_data['openid'],
            self.__request_data['partner_trade_no'],
            self.__request_data['spbill_create_ip'],
            key)
        result = hashlib.md5(raw_string.encode('utf-8')).hexdigest().upper()
        return result

    @staticmethod
    def __generate_trade_sn():
        '''
        生成商户订单号，通常为当前精确到秒的时间+6位随机数字
        :return:
        '''
        chars = string.digits
        rnd = ''.join(random.choice(chars) for _ in range(6))
        return strftime("%Y%m%d%H%M%S", localtime()) + rnd

    @staticmethod
    def __generate_nonce_str(size=30):
        """
        生成随机字符串
        :param size:
        :return:
        """
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def __dict_to_xml(tag, d):
        """
        将Python Dict转换为xml
        """
        elem = Element(tag)
        for key, val in d.items():
            child = Element(key)
            child.text = str(val)
            elem.append(child)
        return elem
