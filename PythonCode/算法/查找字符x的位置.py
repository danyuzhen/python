import time
import random
import sys
import testdata.大文本 as bigText

class func1:
    # 暴力破解
    def func(self, father, child):
        searchNum = 0
        for i in range(0, len(father) - len(child) + 1):
            searchNum = searchNum + 1
            if father[i] == child[0]:
                for j in range(1, len(child)):
                    searchNum = searchNum + 1
                    if father[i + j] != child[j]:
                        break
                    if j == len(child) - 1:
                        return


class func2:
    # sunday demo1
    def func(self, father, child):
        fatherLen = len(father)
        childLen = len(child)
        next = 0
        childDict={}
        for i in range(childLen):
            if child[i] not in childDict.keys():
                childDict[child[i]]=i
        for i in range(fatherLen - childLen):
            i = next
            if father[i] == child[0]:
                for j in range(1, childLen):
                    if father[i + j] != child[j]:
                        if father[i + childLen] in childDict.keys():
                            next = i + childLen - childDict[father[i + childLen]]-1
                        else:
                            next = next + childLen + 1
                        break
                    elif j == childLen - 1:
                        return
            else:
                if father[i + childLen] in childDict.keys():
                    next = i + childLen - childDict[father[i + childLen]]
                else:
                    next = next + childLen + 1


class func3:
    # sunday
    def func(self, father, child):
        len_src = len(father)
        len_dst = len(child)
        i = 0
        while i < len_src - len_dst + 1:
            flag = 0
            shift = len_dst
            for j in range(0, len_dst):
                if father[i + j] != child[j]:
                    flag = -1
                    break

            if flag == 0:
                return i

            p = child.rfind(father[i + shift])
            if p == -1:
                shift = len_dst + 1
            else:
                shift = len_dst - p

            i = i + shift

        return -1


class func4:
    def func(self, string, substring):
        '''
        KMP字符串匹配的主函数
        若存在字串返回字串在字符串中开始的位置下标，或者返回-1
        '''
        pnext = self.gen_pnext(substring)
        n = len(string)
        m = len(substring)
        i, j = 0, 0
        while (i < n) and (j < m):
            if (string[i] == substring[j]):
                i += 1
                j += 1
            elif (j != 0):
                j = pnext[j - 1]
            else:
                i += 1
        if (j == m):
            return i - j
        else:
            return -1

    def gen_pnext(self, substring):
        """
        构造临时数组pnext
        """
        index, m = 0, len(substring)
        pnext = [0] * m
        i = 1
        while i < m:
            if (substring[i] == substring[index]):
                pnext[i] = index + 1
                index += 1
                i += 1
            elif (index != 0):
                index = pnext[index - 1]
            else:
                pnext[i] = 0
                i += 1
        return pnext


# father=''
# for i in range(999999):
#     father=f'{father}{random.randint(0,9)}'
# print(father)
# father = 'substring seearching s search'
father = bigText.bigText1
child = 'search'

st = time.time()
func1().func(father, child)
print('暴力：', time.time() - st)

st = time.time()
func2().func(father, child)
print('my sunday：', time.time() - st)

st = time.time()
func3().func(father, child)
print('sunday：', time.time() - st)

st = time.time()
func4().func(father, child)
print('kmp：', time.time() - st)

st = time.time()
father.find(child)
print('find：', time.time() - st)