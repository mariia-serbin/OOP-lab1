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
    """!
    @brief Insertion Sort algorithm.
    @details Insertion Sort builds the final sorted list one item at a time.
             It iterates over the list and inserts each element into its correct position
             relative to the elements before it. This algorithm is efficient for small datasets
             or lists that are already mostly sorted.
             More info: https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
    """
    def sort(self, data: BaseList)->None:

        """!
        @brief Sorts the given list using insertion sort.
        @param data List to sort (BaseList instance).
        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import InsertionSort

        lst = ArrayList()
        lst.add(5)
        lst.add(2)
        lst.add(8)

        InsertionSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 2 5 8
        @endcode
        """
        size: int = data.size()
        for i in range(size):
            key = data.get(i)
            j = i - 1
            while j >= 0 and data.get(j) > key:
                data.set(j+1, data.get(j))
                j -= 1
            data.set(j+1, key)

class QuickSort(SortingAlgorithm):
    """!
    @brief Quick Sort algorithm.
    @details Quick Sort is a divide-and-conquer sorting algorithm. It works by selecting a "pivot" element
             from the list and partitioning the other elements into two sublists: those less than the pivot
             and those greater than the pivot. The sublists are then recursively sorted. This method is
             efficient for large datasets and has an average time complexity of O(n log n).
             Worst-case time complexity is O(n^2), which can be mitigated by choosing a good pivot strategy.
             More info: https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/
    """
    @staticmethod
    def partition(data: BaseList, lowest: int, highest: int):

        """!
        @brief Partitions the list for Quick Sort.
        @param data List to partition.
        @param lowest Starting index.
        @param highest Ending index.
        @return Index of the pivot element after partition.
        """
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

        """!
        @brief Sorts the list using Quick Sort.
        @param data List to sort.
        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import QuickSort

        lst = ArrayList()
        lst.add(5)
        lst.add(2)
        lst.add(8)

        QuickSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 2 5 8
        @endcode
        """
        self._quick_sort(data, 0, data.size() - 1)

class MergeSort(SortingAlgorithm):
    """!
    @brief Merge Sort algorithm.
    @details Merge Sort is a divide-and-conquer, comparison-based sorting algorithm.
             The list is recursively divided into two halves until each sublist contains a single element.
             Then, the sublists are merged back together in a sorted manner.
             Merge Sort is stable and works efficiently for large datasets with guaranteed O(n log n) time complexity.
             More info: https://www.geeksforgeeks.org/dsa/merge-sort/
    """

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

        """!
        @brief Sorts the list using Merge Sort.
        @param data List to sort.
        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import MergeSort

        lst = ArrayList()
        lst.add(5)
        lst.add(2)
        lst.add(8)

        MergeSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 2 5 8
        @endcode
        """
        self._merge_sort(data, 0, data.size() - 1)

#additional sorting algorithms (Selection, Bubble, 3-way Merge)
class SelectionSort(SortingAlgorithm):
    """!
    @brief Selection Sort algorithm.
    @details Selection Sort is a comparison-based sorting algorithm.
             The main idea is to repeatedly find the minimum element from the unsorted part of the list
             and move it to the beginning. This process continues until the list is fully sorted.
             Selection Sort is not stable and has a time complexity of O(n^2), making it inefficient
             for large datasets.
             More info: https://www.geeksforgeeks.org/dsa/selection-sort-algorithm-2/
    """
    def sort(self, data: BaseList) -> None:
        """!
        @brief Sorts the list using Selection Sort.
        @param data List to sort (BaseList instance).
        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import SelectionSort

        lst = ArrayList()
        lst.add(5)
        lst.add(2)
        lst.add(8)

        SelectionSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 2 5 8
        @endcode
        """
        n: int = data.size()
        for i in range(n):
            min_index: int = i
            for j in range(i + 1, n):
                if data.get(j) < data.get(min_index):
                    min_index = j

            data.swap(i, min_index)

class BubbleSort(SortingAlgorithm):
    """!
    @brief Bubble Sort algorithm.
    @details Bubble Sort is a simple comparison-based sorting algorithm.
             The main idea is to repeatedly iterate through the list,
             compare adjacent elements, and swap them if they are in the wrong order.
             As a result, larger elements "bubble up" to the end of the list.

             Bubble Sort is stable, but it has a time complexity of O(n^2),
             which makes it inefficient for large datasets. It is mainly used
             for educational purposes or very small inputs.

             More info: https://www.geeksforgeeks.org/dsa/bubble-sort-algorithm/
    """
    def sort(self, data: BaseList) -> None:
        """!
        @brief Sorts the list using Bubble Sort.
        @param data List to sort (BaseList instance).
        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import BubbleSort

        lst = ArrayList()
        lst.add(3)
        lst.add(1)
        lst.add(4)

        BubbleSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 1 3 4
        @endcode
        """
        size: int = data.size()
        for i in range(size):
            for j in range(i + 1, size):
                if data.get(j) < data.get(i):
                    data.swap(i, j)

class ThreeWayMergeSort(SortingAlgorithm):

    """!
    @brief Three-Way Merge Sort algorithm.
    @details Three-Way Merge Sort is an extended version of the classic Merge Sort.
             Instead of splitting the array into 2 parts, this algorithm splits it into
             **three equal segments**, recursively sorts each of them, and then merges
             the three sorted segments into one.

             The main idea is reducing the depth of recursion by increasing the number
             of partitions. The algorithm still maintains a time complexity of O(n log n),
             but with base 3 instead of 2, which leads to slightly fewer recursion levels.

             This algorithm is stable and performs well on large datasets; however,
             its memory usage is higher due to additional temporary lists.

             More info: https://www.geeksforgeeks.org/dsa/3-way-merge-sort/
    """
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

        """!
        @brief Sorts the list using Three-Way Merge Sort.
        @param data List to sort (BaseList instance).

        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import ThreeWayMergeSort

        lst = ArrayList()
        lst.add(9)
        lst.add(3)
        lst.add(7)
        lst.add(1)

        ThreeWayMergeSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 1 3 7 9
        @endcode
        """
        self._three_way_merge(data, 0, data.size() - 1)

#additional sorting algorithms (non-comparison). Bucket Sort, Count Sort

class BucketSort(SortingAlgorithm):
    """!
    @brief Bucket Sort algorithm.
    @details Bucket Sort is a distribution-based sorting algorithm.
             It divides all input elements into a fixed number of "buckets"
             based on their value range. Each bucket stores elements that fall
             into the same interval. After distribution, each bucket is sorted
             individually (commonly using Insertion Sort), and finally all
             buckets are concatenated to form the final sorted list.

             This algorithm is most efficient when sorting uniformly distributed
             floating-point or integer data. In the best case it works in O(n)
             time, but performance depends heavily on choosing an appropriate
             number of buckets.

             More info: https://www.geeksforgeeks.org/dsa/bucket-sort-2/
    """

    def sort(self, data: BaseList, num_buckets: Optional[int] = None):

        """!
        @brief Sorts the list using Bucket Sort.
        @param data List to sort (BaseList instance).
        @param num_buckets Optional manual specification of the number of buckets.
                           If not provided, it is chosen automatically based on the
                           data size.

        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import BucketSort

        lst = ArrayList()
        lst.add(0.25)
        lst.add(0.1)
        lst.add(0.9)
        lst.add(0.4)

        BucketSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 0.1 0.25 0.4 0.9
        @endcode
        """
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
    """!
    @brief Counting Sort algorithm.
    @details Counting Sort is an integer sorting algorithm that works by counting
             the number of occurrences of each value in the input list.

             The main idea is to create an auxiliary array (count array) where each
             index corresponds to a value from the input, and stores how many times
             that value appears. Then, using prefix sums, the algorithm determines
             the correct position of each element in the output list.

             Counting Sort runs in O(n + k) time, where k is the range of input
             values. It is extremely efficient when the range of values is small
             relative to the number of elements. The algorithm is stable if
             implemented from right to left (as in this version).

             More info: https://www.geeksforgeeks.org/dsa/counting-sort/
    """
    def sort(self, data: BaseList) -> None:

        """!
        @brief Sorts the list using Counting Sort.
        @param data List to sort (BaseList instance). Must contain **non-negative integers**.

        @par Example:
        @code
        from lists import ArrayList
        from sorting_algorithms import CountSort

        lst = ArrayList()
        lst.add(4)
        lst.add(2)
        lst.add(2)
        lst.add(1)

        CountSort().sort(lst)

        for i in range(lst.size()):
            print(lst.get(i))
        # Output: 1 2 2 4
        @endcode
        """
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

