import random
import time


def func1():
    for i in a:
        dicta[i] = 0
    for i in b:
        if i in dicta.keys():
            del b[i]


def func2():
    for i in a:
        dicta[i] = 0
    for i in b:
        dicta[i] = 0
    for k,v in dictb.items():
        if k in dicta.keys():
            dictb.pop(k)

def func3():
    for i in a:
        b.append(1)
    print(len(b))


a = []
b = []
dicta = {}
dictb = {}

for i in range(1000000):
    a.append(random.randint(0, 1000000))
for i in range(10000000):
    b.append(0)

# st = time.time()
# func1()
# print(time.time() - st)
#
# st = time.time()
# func2()
# print(time.time() - st)
print('st')
st = time.time()
func3()
print(time.time() - st)
