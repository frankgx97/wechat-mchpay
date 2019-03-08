# Wechat-MchPay

微信支付企业付款SDK

## 安装
```
pip install wechat_mchpay
```

## 使用

```
#coding:utf8

from wechat_mchpay import MchPay

"""
appid: 与商户绑定的appid
mchid: 微信支付商户id
api_key: 微信支付后台设置的商户key
cert_path: 从商户后台下载的微信支付api证书的路径。其文件名为apiclient_cert.pem。
key_path: 从商户后台下载的微信支付api私钥的路径。其文件名为apiclient_key.pem。
"""
pay = MchPay(appid, mchid, api_key, cert_path, key_path)

"""
openid: 目标付款用户的openid
amount: 付款金额，单位为分
desc: 付款描述
trade_no: 商户交易单号。正常情况下无需传入，系统会自动生成一个由当前的精确到秒的时间加上6为随机数字组成的商户单号。如果要重试之前失败的交易，则简易传入之前的交易单号。
ip: 当前发起请求的ip地址。如果留空，则会自动获取。自动获取的速度较慢，建议在生产环境中传入ip。
"""
pay.setup(openid, amount, desc, trade_no="", ip="124.64.19.132")

result = pay.send()
"""
result返回一个包含四个元素的数组，分别为：结果（'success'/'fail），错误码，错误信息，商户单号。
"""
print(result)
```

### LICENCE
MIT Licence