from abc import ABC, abstractmethod
from lists import *

class Sequence(ABC):

    """
    Sequence class is an abstract class made for easier implementing sequences.
    Methods:
        first_k_elements(k): returns list of first k elements of sequence.
        is_bounded(): returns True if sequence is bounded and False otherwise.
        is_monotonic(): returns True if sequence is monotonic and False otherwise.
        limit(to_inf): returns limit of sequence if to_inf is True.
    """
    @abstractmethod
    def first_k_elements(self, k):
        pass

    @abstractmethod
    def is_monotonic(self, is_decreasing = None):
        pass

    @abstractmethod
    def is_bounded(self):
        pass

    @abstractmethod
    def limit(self, to_inf = True):
        pass

    @abstractmethod
    def partial_sum(self, n):
        pass


class ManualSequence(Sequence):
    def __init__(self, list_type):
        self.sequence = list_type()
        self.is_bounded = True
        self.is_convergent = False
        self.length = 0

    def get_sequence(self):
        input_sequence = input("Enter elements of your sequence (no separators needed): ")
        input_sequence = input_sequence.split()
        for item in input_sequence:
            self.sequence.add(item)

        self.length = self.sequence.size()

    def first_k_elements(self, k):
        if k > self.length:
            raise ValueError

        result = type(self.sequence)()
        for i in range(k):
            result.add(self.sequence.get(i))
        return result

    def _is_increasing(self):
        is_increasing = False
        for i in range(0, self.length):
            if self.sequence.get(i) < self.sequence.get(i+1):
                is_increasing = True

        return is_increasing

    def _is_decreasing(self):
        is_decreasing = False
        for i in range(0, self.length):
            if self.sequence.get(i) > self.sequence.get(i + 1):
                is_decreasing = True

        return is_decreasing


    def is_monotonic(self, is_increasing = None):
        if is_increasing:
            increasing = self._is_increasing()
            return increasing
        elif not is_increasing:
            decreasing = self._is_decreasing()
            return decreasing
        else:
            is_monotonic = False
            if self._is_decreasing() or self._is_increasing():
                is_monotonic = True

            return is_monotonic

    def is_bounded(self):
        if self.sequence.size() < 0:
            raise IndexError
        if self.sequence.min() or self.sequence.max():
            return True

        return False

    def limit(self, to_inf = True):
        if to_inf:
            if self.is_monotonic(True):
                return self.sequence.get(self.length - 1)
            else:
                raise ValueError("This sequence is not monotonic")

        else:
            if self.is_monotonic(False):
                return self.sequence.get(self.length - 1)
            else:
                raise ValueError("This sequence is not monotonic")

    def partial_sum(self, n):
        partitial_sum = 0
        for i in range(n):
            partitial_sum += self.sequence.get(i)

        return partitial_sum







