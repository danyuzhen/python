# 数组里有{1,2,3,4,5,6,7,8,9,10}，请随机打乱顺序，生成一个新的数组。
def a():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(int(len(list1) / 2)):
        list1[i], list1[-i] = list1[-i], list1[i]
    print(list1)


# 写出代码判断一个整数是不是2的阶次方。
def b():
    num = 128
    if num % 2 == 0:
        print('yes')
    else:
        print('no')


# 假设今日是2015年3月1日，星期日，请算出13个月零6天后是星期几，距离现在多少秒。
def c():
    oldDate = [2015, 3, 1, 7]
    newDate = [2015, 3, 1, 7]
    addMonth = 13
    addDay = 6
    if newDate[1] + addMonth > 12:
        newDate[0] = newDate[0] + int((newDate[1] + addMonth) / 12)
        newDate[1] = (newDate[1] + addMonth) % 12

    day = newDate[2] + addDay
    if newDate[1] == 2:
        monthMax = 28
        if (newDate[0] % 4 == 0 and newDate[0] % 100 != 0) or newDate[0] % 400 == 0:
            monthMax = 29
        if day > monthMax:
            newDate[1] += 1
            newDate[2] = day % monthMax
        else:
            newDate[2] = day
    else:
        monthMax = 30
        if newDate[1] in [1, 3, 5, 7, 8, 10, 12]:
            monthMax = 31
        if day > monthMax:
            newDate[1] += 1
            newDate[2] = day % monthMax
        else:
            newDate[2] = day

    totalDay = addDay
    for i in range(oldDate[1], oldDate[1] + addMonth):
        nowYear = oldDate[0] + int(i / 12)
        nowMonth = 12 if (i % 12) == 0 else (i % 12)
        if nowMonth == 2:
            monthMax = 28
            if (nowYear % 4 == 0 and nowYear % 100 != 0) or nowYear % 400 == 0:
                monthMax = 29
            totalDay += monthMax
        else:
            monthMax = 30
            if nowMonth in [1, 3, 5, 7, 8, 10, 12]:
                monthMax = 31
            totalDay += monthMax

    newDate[-1] = totalDay % 7
    totalSecond = totalDay * 3600 * 24

    print(newDate[-1])
    print(totalSecond)


# 实现一个排序方法,能对任意单一类型数组排序.
def quick_sort(list1):
    return q_sort(list1, 0, len(list1) - 1)


def q_sort(list1, left, right):
    if left < right:
        pivot = Partition(list1, left, right)
        q_sort(list1, left, pivot - 1)
        q_sort(list1, pivot + 1, right)
    return list1


def Partition(list1, left, right):
    pivotkey = list1[left]
    print(left, right)
    while left < right:
        while left < right and list1[right] >= pivotkey:
            right -= 1
        list1[left] = list1[right]
        while left < right and list1[left] <= pivotkey:
            left += 1
        list1[right] = list1[left]

    list1[left] = pivotkey
    return left


def start():
    list1 = [5, 3, 1, 11, 6, 7, 2, 4]
    res = quick_sort(list1)
    print(res)


a()
b()
c()
