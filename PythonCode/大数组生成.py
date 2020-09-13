import time
import random


def create_list():
    a=[]
    for i in range(1000):
        a.append(random.randint(1,99999999))
    f = open('testdata/千数组.txt', 'w+')
    f.write(str(a))
    f.close()

def maopao():
    for i in range(lena - 1):
        for j in range(i, lena):
            if a[j] < a[i]:
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
        

st = time.time()
f = open('testdata/千数组.txt', 'r')
a = eval(f.read())
lena = len(a)
en = time.time() - st
print(f'加载完成。耗时：{en}')

st = time.time()
maopao()
en = time.time() - st
print(f'冒泡排序完成。耗时：{en}')

st = time.time()
sorted(a)
en = time.time() - st
print(f'timeout排序完成。耗时：{en}')
