from abc import ABC, abstractmethod
from lists import BaseList
#abstract class for sorting algorithms
class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, data):
        pass

#must do sorting algorithms (Insertion, Quick, Merge)
class InsertionSort(SortingAlgorithm):
    """
    Insertion Sort algorithm.
    Methods:
        sort(data: BaseList) -> BaseList: sorts list using insertion sort.
    """
    def sort(self, data: BaseList):
        size = data.size
        for i in range(size):
            key = data.get(i)
            j = i - 1
            while j >= 0 and data.get(j) > key:
                data.set(j+1, data.get(j))
                j -= 1
            data.set(j+1, key)

class QuickSort(SortingAlgorithm):
    """"
    Quick Sort algorithm.
    Methods:
        sort(data: BaseList) -> BaseList: sorts list using quick sort and uses protected methods:
            _partition(data:BaseList, lowest: int, highest: int) -> BaseList: for partition
            _quick_sort(data: BaseList, lowest: int, highest: int) -> BaseList: realization of quick sort
    """
    def _partition(self, data, lowest: int, highest: int):
        pivot = data.get(highest)
        i = lowest - 1

        for j in range(lowest, highest):
            if data.get(j) < pivot:
                i = i + 1
                data.swap(i, j)

        data.swap(i + 1, highest)

        return i + 1

    def _quick_sort(self, data, lowest, highest):
        if lowest < highest:
            pivot_index = self._partition(data, lowest, highest)

            self._quick_sort(data, lowest, pivot_index - 1)
            self._quick_sort(data, pivot_index + 1, highest)

    def sort(self, data: BaseList):
        self._quick_sort(data, 0, data.size() - 1)

class MergeSort(SortingAlgorithm):
    def _merge(self, data: BaseList, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        Left = type(data)()
        Right = type(data)()

        for i in range(n1):
            Left.add(data.get(left + i))

        for j in range(n2):
            Right.add(data.get(mid + j + 1))

        i, j = 0
        k = left

        while i < n1 and j < n2:
            if Left.get(i) < Right.get(j):
                data.set(k, Left.get(i))
                i += 1
            else:
                data.set(k, Right.get(j))
                j += 1
            k += 1

        while i < n1:
            data.set(k, Left.get(i))
            i += 1
            k += 1

        while j < n2:
            data.set(k, Right.get(j))
            j += 1
            k += 1

    def _merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2

            self._merge_sort(data, left, mid)
            self._merge_sort(data, mid + 1, right)
            self._merge(data, left, mid, right)

    def sort(self, data: BaseList):
        self._merge_sort(data, 0, data.size() - 1)

#additional sorting algorithms (Selection, Bubble, 3-way Merge)
class SelectionSort(SortingAlgorithm):
    def sort(self, data: BaseList):
        n = data.size()
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if data.get(j) < data.get(min_index):
                    min_index = j

            data.swap(i, min_index)

class BubbleSort(SortingAlgorithm):
    def sort(self, data):
        size = data.size()
        for i in range(size):
            for j in range(i + 1, size):
                if data.get(j) < data.get(i):
                    data.swap(i, j)

class ThreeWayMergeSort(SortingAlgorithm):
    def _merge(self, data, left, mid1, mid2, right):
        size1 = mid1 - left + 1
        size2 = mid2 - mid1
        size3 = right - mid2

        #temporary lists for 3 parts
        left_list = type(data)()
        middle_list = type(data)()
        right_list = type(data)()

        i = j = k = 0
        index = left

        while i < size1 or j < size2 or k < size3:

            min_value = float('inf')
            min_index = -1

            if i < size1 and left_list.get(i) < min_value:
                min_value = left_list.get(i)
                min_index = 0
            elif j < size2 and middle_list.get(j) < min_value:
                min_value = middle_list.get(j)
                min_value = 1
            elif k < size3 and right_list.get(k) < min_value:
                min_value = right_list.get(k)
                min_index = 2

            if min_index == 0:
                data.set(index, left_list.get(i))
                index += 1
            elif min_index == 1:
                data.set(index, middle_list.get(j))
                j += 1
            else:
                data.set(index, right_list.get(k))
                k += 1

            index += 1

    def _three_way_merge(self, data, left, right):

        if left < right:
            left, right = right, left

        mid1 = left + (right - left) // 3
        mid2 = left + 2*(right - left) // 3

        self._three_way_merge(data, left, mid1)
        self._three_way_merge(data, mid1 + 1, mid2)
        self._three_way_merge(data, mid2 + 1, right)

        self._merge(data, left, mid1, mid2, right)

    def sort(self, data: BaseList):
        self._three_way_merge()

#additional sorting algorithms (non-comparison). Bucket Sort, Radix Sort
