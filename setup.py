#coding:utf8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wechat_mchpay',
    version='0.0.7',
    author='nyanim',
    author_email='i@nyan.im',
    url='https://github.com/nyanim/wechat-mchpay',
    description=u'微信支付企业付款SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'xmltodict==0.12.0'
        'requests==2.21.0'
    ],
    entry_points={}
)