import random
import time

def func1(a, target):
    res=[target]
    for i in range(len(a)):
        for j in range(i, len(a)):
            if a[i] + a[j] == target:
                res.append([a[i], a[j]])
                return res

def func2(a, target):
    dicta={}
    res = [target]
    for i in a:
        dicta[i]=0
    for k,v in dicta.items():
        if target-k in dicta.keys():
            res.append([k, target-k])
            return res


a = [i for i in range(10000)]
target = random.randint(0, 19999)

st=time.time()
res=func1(a, target)
print(res)
print(time.time()-st)

st=time.time()
res=func2(a, target)
print(res)
print(time.time()-st)
