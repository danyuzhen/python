import threading
import random
import queue
import copy

class Action:
    def __init__(self, threadname):
        self.name = threadname

    def run(self):
        # print('name:',self.name)
        # print('qzise:',queue.qsize())
        list1=[x for x in range(10)]
        random.shuffle(list1)
        msgDict=queue.get()
        msgDict[0]=list1
        print(msgDict)
        queue.put(msgDict)

class Action1:

    def __init__(self, threadname):
        self.name = threadname

    def run(self):
        # print('name:',self.name)
        # print('qzise:',queue.qsize())
        msgDict=queue.get()
        list1=copy.copy(msgDict[0])
        for i in range(len(list1)):
            list1[i]=list1[i]+1
        msgDict[1]=list1
        queue.put(msgDict)


if __name__ == '__main__':
    list1 = [x for x in range(1, 31)]
    msgDict = {}
    queue = queue.Queue()
    queue.put(msgDict)
    p = threading.Thread(target=Action('main').run())
    p.start()
    p.join()
    p = threading.Thread(target=Action1('slave').run())
    p.start()
    p.join()
    print(msgDict)
