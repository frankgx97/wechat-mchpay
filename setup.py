#coding:utf8

from setuptools import setup

setup(
    name='wechat-mchpay',
    version='0.0.1',
    author='nyanim  ',
    author_email='i@nyan.im',
    url='https://github.com/nyanim/wechat_mchpay',
    description=u'微信支付企业付款SDK',
    packages=['wechat-mchpay'],
    install_requires=[
        'xmltodict==0.12.0'
        'requests==2.21.0'
    ],
    entry_points={}
)