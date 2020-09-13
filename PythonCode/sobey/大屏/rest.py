#!/usr/bin/env python3
# coding: utf-8
import json
from datetime import datetime, timedelta
import base64
import hmac
from hashlib import sha1
import requests

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
site_code = operate_site = "S1"
system_code = "MAM"
system_secret_key = "e2c84557fc9c4d069bfc7b958abccdca"
user_code = "admin"
url = "http://172.16.149.73:88/sobeyhive-bp/v1/search"
contenttype = 'application/json'

def get_entityinfo_url(data):
    data = json.dumps(data)
    dateStr = (datetime.utcnow() - timedelta(minutes=0)).strftime(GMT_FORMAT)
    sign = get_request_signature_header('POST', dateStr, contenttype)
    headers = {
        'sobeyhive-http-site': site_code,
        'sobeyhive-http-date': dateStr,
        'sobeyhive-http-authorization': sign,
        'sobeyhive-http-system': system_code,
        'Content-Type': contenttype,
        'current-user-code': user_code
    }
    res = requests.post(url, headers=headers, data=data)
    return res.json()


def get_request_signature_header(method, dateStr, contenttype='application/json'):
    sign = __get_request_signature(
        method, '', system_secret_key, dateStr, contenttype)

    return 'SobeyHive {system_code}:{sign}'.format(system_code=system_code, sign=sign)


def __get_request_signature(method, conentmd5, encryptKey, dateStr, contenttype='application/json'):
    stringToSign = '{method}\n{conentmd5}\n{contenttype}\n{dateStr}' \
        .format(method=method, conentmd5=conentmd5, contenttype=contenttype, dateStr=dateStr)

    hmac_code = hmac.new(encryptKey.encode(), stringToSign.encode(), sha1)
    signature = base64.b64encode(hmac_code.digest())
    # 去调签名的 b
    return str(signature, 'utf8')

# s = get_entityinfo_url(data)
# print(s)
# for i in s['extensionResults'][0]['values']:
#     print(i)
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(s, f, ensure_ascii=False)
