from abc import ABC, abstractmethod
from lists import BaseList

class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, data):
        pass

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


