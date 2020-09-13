class mydemo:
    list1 = [1, 5, 2, 34, 8, 6, 17, 9]

    def quick(self, list1, left, right):
        if left != right:
            pass

    def doquick(self, list1, left, right):
        basic = list1[left]
        for i in range(left, right):
            if list1[right] > basic:
                pass


class demo1:
    0

    def start(self):
        list1 = [2, 8, 7, 1, 3, 5, 6, 14]
        list1 = [5, 2, 7, 1, 4, 6, 7, 8, 1]
        self.quicksort(list1, 0, len(list1) - 1)
        print(list1)


class demo2:
    def q_sort(self, L, left, right):
        print('q_sort开始：', L, 'l:', left, 'r:', right)
        if left < right:
            print('left<right')
            pivot = self.Partition(L, left, right)
            print('下次的pivot', pivot, '\n')

            self.q_sort(L, left, pivot - 1)
            self.q_sort(L, pivot + 1, right)
        print('q_sort结束：', L, '\n')
        return L

    def Partition(self, L, left, right):
        pivotkey = L[left]
        print('原始：', L, 'left:', left, 'right:', right, 'p:', pivotkey)
        while left < right:
            while left < right and L[right] >= pivotkey:
                right -= 1
            L[left] = L[right]
            print('右操作：', L, 'left:', left, 'right:', right)

            while left < right and L[left] <= pivotkey:
                left += 1
            L[right] = L[left]
            print('左操作：', L, 'left:', left, 'right:', right)

        L[left] = pivotkey
        print('结束：', L, 'left:', left, 'right:', right)
        return left

    def start(self):
        L = [5, 3, 1, 11, 6, 7, 2, 4]
        res = self.q_sort(L, 0, len(L) - 1)
        print(res)


demo1().start()
