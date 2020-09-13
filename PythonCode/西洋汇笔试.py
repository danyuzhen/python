import re
import random
import time


def t1():
    text = "请编写一个正则表达式，要求能把以下这四种格式字符串：“$200.49、“$1,999.00”、“$99”、“50.00美元”从一段文本中匹配出来。（不需要考虑千分位及小数点的位置校验）"
    pricePattern = re.compile('\$?[.,\d]+[美元]{0,2}')
    print(pricePattern.findall(text))


def t2():
    num = [str(i) for i in range(0, 10)]
    list1 = ['1.409,00', '409,05', '409.50', '1,000']
    priceList = []
    for i in list1:
        if i[-3] not in num:
            integer = ''
            for j in i[:-3]:
                if j in num:
                    integer += j
            if int(i[-2:]) != 0:
                price = float(integer + '.' + i[-2:])
            else:
                price = int(integer)
            priceList.append(price)
        else:
            integer = ''
            for j in i:
                if j in num:
                    integer += j
            priceList.append(int(integer))
    print(priceList)


def t3():
    # 无法命令行输入，使用随机生成100行100列数组为初始矩阵
    rowNum = 1000
    arr = []
    for i in range(rowNum):
        randomList = []
        for j in range(rowNum):
            randomList.append(random.randint(1, 100))
        random.shuffle(randomList)
        arr.append(randomList)

    num1 = 0
    num2 = 0
    for i in range(rowNum):
        for j in range(i, rowNum):
            num1 += arr[i][j]
            num2 += arr[rowNum - i - 1][j]
            break
    print(abs(num1 - num2))


# t1()
# t2()
t3()
