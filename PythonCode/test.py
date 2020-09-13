def a(num):
    print('原始:', num)
    if num < 10:
        num = b(num)
        print('计算:', num)
        a(num)
        print(1)
        a(num)
    return num


def b(num):
    num = num + 1
    return num


def c():
    num = 0
    res = a(num)
    print('res:', res)


c()
