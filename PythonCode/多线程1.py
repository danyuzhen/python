import threading
import random
import queue
import time

class Action:
    def __init__(self, threadname):
        self.name = threadname

    def run(self):
        for i in range(10):
            list1=[x for x in range(10000)]
            random.shuffle(list1)
            msgDict=queue.get()
            msgDict[0].append(list1)
            queue.put(msgDict)

class Action1:

    def __init__(self, threadname):
        self.name = threadname

    def run(self):
        msgDict=queue.get()
        list1=msgDict[0].pop(0)
        for i in range(len(list1)):
            list1[i]=list1[i]+1
        msgDict[1].append(list1)
        queue.put(msgDict)


if __name__ == '__main__':
    st=time.time()
    list1 = [x for x in range(1, 31)]
    msgDict = {0: [], 1: [],2:[]}
    queue = queue.Queue()
    queue.put(msgDict)
    p = threading.Thread(target=Action('main').run())
    p.start()
    p.join()
    p = threading.Thread(target=Action1('slave').run())
    p.start()
    p.join()
    print(time.time()-st)
