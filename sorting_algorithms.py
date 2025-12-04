from abc import ABC, abstractmethod
from lists import BaseList
from typing import Optional, List
#abstract class for sorting algorithms
class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, data: BaseList):
        pass

#must do sorting algorithms (Insertion, Quick, Merge)
class InsertionSort(SortingAlgorithm):
    """
    Insertion Sort algorithm.
    Methods:
        sort(data: BaseList) -> BaseList: sorts list using insertion sort.
    """
    def sort(self, data: BaseList)->None:
        size: int = data.size()
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
    @staticmethod
    def partition(data: BaseList, lowest: int, highest: int):
        pivot = data.get(highest)
        i = lowest - 1

        for j in range(lowest, highest):
            if data.get(j) < pivot:
                i = i + 1
                data.swap(i, j)

        data.swap(i + 1, highest)

        return i + 1

    def _quick_sort(self, data: BaseList, lowest: int, highest: int) -> None:
        if lowest < highest:
            pivot_index = self._partition(data, lowest, highest) # type: ignore

            self._quick_sort(data, lowest, pivot_index - 1)
            self._quick_sort(data, pivot_index + 1, highest)

    def sort(self, data: BaseList) -> None:
        self._quick_sort(data, 0, data.size() - 1)

class MergeSort(SortingAlgorithm):
    @staticmethod
    def _merge(data: BaseList, left_idx, mid_idx, right_idx):
        n1: int = mid_idx - left_idx + 1
        n2: int = right_idx - mid_idx

        left: BaseList = type(data)()
        right: BaseList = type(data)()

        for i in range(n1):
            left.add(data.get(left_idx + i))

        for j in range(n2):
            right.add(data.get(mid_idx + j + 1))

        i, j = 0, 0
        k = left_idx

        while i < n1 and j < n2:
            if left.get(i) < right.get(j):
                data.set(k, left.get(i))
                i += 1
            else:
                data.set(k, right.get(j))
                j += 1
            k += 1

        while i < n1:
            data.set(k, left.get(i))
            i += 1
            k += 1

        while j < n2:
            data.set(k, right.get(j))
            j += 1
            k += 1

    def _merge_sort(self, data, left, right):
        if left < right:
            mid:  int = (left + right) // 2

            self._merge_sort(data, left, mid)
            self._merge_sort(data, mid + 1, right)
            self._merge(data, left, mid, right)

    def sort(self, data: BaseList) -> None:
        self._merge_sort(data, 0, data.size() - 1)

#additional sorting algorithms (Selection, Bubble, 3-way Merge)
class SelectionSort(SortingAlgorithm):
    def sort(self, data: BaseList) -> None:
        n: int = data.size()
        for i in range(n):
            min_index: int = i
            for j in range(i + 1, n):
                if data.get(j) < data.get(min_index):
                    min_index = j

            data.swap(i, min_index)

class BubbleSort(SortingAlgorithm):
    def sort(self, data: BaseList) -> None:
        size: int = data.size()
        for i in range(size):
            for j in range(i + 1, size):
                if data.get(j) < data.get(i):
                    data.swap(i, j)

class ThreeWayMergeSort(SortingAlgorithm):
    @staticmethod
    def _merge(data: BaseList, left: int, mid1: int, mid2: int, right: int) -> None:
        size1 = mid1 - left + 1
        size2 = mid2 - mid1
        size3 = right - mid2

        #temporary lists for 3 parts
        left_list: BaseList = type(data)()
        middle_list: BaseList = type(data)()
        right_list: BaseList = type(data)()

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
                min_index = 1
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

    def _three_way_merge(self, data: BaseList, left: int, right: int):

        if left >= right: return

        mid1 = left + (right - left) // 3
        mid2 = left + 2*(right - left) // 3

        self._three_way_merge(data, left, mid1)
        self._three_way_merge(data, mid1 + 1, mid2)
        self._three_way_merge(data, mid2 + 1, right)

        self._merge(data, left, mid1, mid2, right)

    def sort(self, data: BaseList) -> None:
        self._three_way_merge(data, 0, data.size() - 1)

#additional sorting algorithms (non-comparison). Bucket Sort, Count Sort

class BucketSort(SortingAlgorithm):

    def sort(self, data: BaseList, num_buckets: Optional[int] = None):
        n = data.size()
        if n == 0:
            return data

        if not num_buckets:
            num_buckets = int(n ** 0.5) + 1

        min_val: float= data.get(0)
        max_val: float = data.get(0)
        for i in range(1, n):
            val = data.get(i)
            if val < min_val:
                min_val = val
            if val > max_val:
                max_val = val

        range_size: float = (max_val - min_val + 1) / num_buckets

        buckets: list[BaseList] = [type(data)() for _ in range(num_buckets)]

        for i in range(n):
            value:float = data.get(i)
            index: int  = int((value - min_val) / range_size)
            if index == num_buckets:
                index -= 1
            buckets[index].add(value)

        for b in buckets:
            InsertionSort().sort(b)

        index: int = 0
        for b in buckets:
            for i in range(b.size()):
                data.set(index, b.get(i))
                index += 1

        return data

class CountSort(SortingAlgorithm):
    def sort(self, data: BaseList) -> None:
        n: int = data.size()

        max_val: int = data.max()

        cnt_arr: List[int] = [0] * (max_val + 1)

        for i in range(n):
            cnt_arr[data.get(i)] += 1

        for i in range(1, max_val + 1):
            cnt_arr[i] += cnt_arr[i - 1]

        ans: BaseList = type(data)()
        for _ in range(n):
            ans.add(0)

        for i in range(n - 1, -1, -1):
            v: int = data.get(i)
            index: int = cnt_arr[v] - 1
            ans.set(index, v)
            cnt_arr[v] -= 1

        for i in range(n):
            data.set(i, ans.get(i))

