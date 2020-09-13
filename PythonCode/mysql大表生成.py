import pymysql
import random
import threading
import time

def start():
    loadst=time.time()
    f = open('testdata/千万数组.txt', 'r').read()
    file = eval(f)
    loaded = time.time()
    print('读取耗时：',round(loaded-loadst, 3))
    thread = []
    threadiNum=100
    threadst = time.time()
    for i in range(threadiNum):
        db = pymysql.connect("47.102.141.184", "root", "123456", "test")
        cursor = db.cursor()
        st = int(i * len(file)/threadiNum)
        ed = int((i + 1) * len(file)/threadiNum)
        flist = file[st:ed]
        p = threading.Thread(target=do, args=(db, cursor, flist,st,))
        thread.append(p)
    for i in thread:
        i.start()
    for i in thread:
        i.join()
    threaded = time.time()
    print('插入耗时：', round(threaded - threadst, 3))

def do(db, cursor, f,st):
    for i in range(len(f)):
        uid = st+i
        name = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz123456789', 10))
        money = f[i]
        sql = f'INSERT into test_10000000(userId,userName,money) values({uid},"{name}",{money});'
        try:
            cursor.execute(sql)
            db.commit()
            print('ok:', i)
        except:
            print('err:', sql)
    cursor.close()
    db.close()


start()
