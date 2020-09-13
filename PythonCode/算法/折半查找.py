# 返回 x 在 arr 中的索引，如果不存在返回 -1
def binarySearch(arr, l, r, x):
    print(l, r, x)
    if r >= l:
        mid = int((r + l) / 2)
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return -1


# 测试数组
5
arr = [1, 3, 5, 7, 9]
# x = [2, 5, 10]
x = [10]
# 函数调用
for i in x:
    result = binarySearch(arr, 0, len(arr) - 1, i)
    print(result)
