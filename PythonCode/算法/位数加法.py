# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 11:07:58 2019

@author: Admin
位数加法
"""

from functools import reduce#导入reduce用于将整数列表中的内容转换为字符串
def add(a, b):
    if len(a) > len(b):#将输入的数字左端补齐为同样的长度
        b = b.zfill(len(a) - len(b) + 1)
    else:
        a = a.zfill(len(b) - len(a) + 1)
    #("0" + str(a))前面加"0"的原因是防止最高位进位是超过列表的容量限制
    #比如说9+9会向前面进一位,如果没有添加额外的0的话进位1就没地方存储
    a = list(map(lambda x : int(x), ("0" + str(a)).strip()))
    b = list(map(lambda x : int(x), ("0" + str(b)).strip()))
    for i in range(len(a) - 1, 0, -1):
        temp = a[i] + b[i];
        print(temp)
        a[i - 1] += temp // 10
        a[i] = temp % 10
    print(a)
    return int(reduce(lambda x, y : str(x) + str(y), a))#转换为字符串

print(add('1200','1400'))