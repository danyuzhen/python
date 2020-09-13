import random
import time


def func1(a, b,lena):
    dicta = {}
    dictb = {}
    c=[]
    for i in range(lena):
        dicta[a[i]] = 0
        dictb[b[i]] = 0

    for k,v in dictb.items():
        if k in dicta.keys():
            c.append(k)
    print(len(c))

a = []
b = []
listLen=1000000
for i in range(listLen):
    a.append(random.randint(0, listLen))
    b.append(random.randint(0, 2*listLen))

st=time.time()
func1(a, b,listLen)
print((time.time()-st))
