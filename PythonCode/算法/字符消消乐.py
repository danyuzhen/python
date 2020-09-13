# 行数，每行消除几次，最短消除重复数，行内容*
# 循环次数为字符长度-1，初始化左右指针，左为当前字符，右为下一个，
# 当左右相等时，以右指针下标为起点，往后循环，找到最后一个相同字符的下标，如果最后下标-左节点>1(最小重复消除数)，删除这段字符
title = [3, 2, 2, 'abbbceec', 'dbbdd', 'abb']

for i in range(3, 3 + title[0]):
    delStr = title[i]
    for delNum in range(title[1]):
        strLen = len(delStr)
        for charInt in range(strLen - 1):
            left = delStr[charInt]
            right = delStr[charInt + 1]
            if left == right:
                lastIndex = charInt + 1
                for j in range(charInt + 1, strLen):
                    if delStr[j] == left:
                        lastIndex = j
                    else:
                        break
                if lastIndex - charInt >= title[2] - 1:
                    delStr = delStr[:charInt] + delStr[lastIndex + 1:]
                    break
    print(delStr)
