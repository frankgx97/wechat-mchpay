#coding:utf8

import setuptools

setuptools.setup(
    name='wechat_mchpay',
    version='0.0.5',
    author='nyanim  ',
    author_email='i@nyan.im',
    url='https://github.com/nyanim/wechat-mchpay',
    description=u'微信支付企业付款SDK',
    packages=setuptools.find_packages(),
    install_requires=[
        'xmltodict==0.12.0'
        'requests==2.21.0'
    ],
    entry_points={}
)