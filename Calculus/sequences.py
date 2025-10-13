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
        self.is_convergent = False
        self.length = 0

    def get_sequence(self):
        input_sequence = input("Enter elements of your sequence (no separators needed): ")
        input_sequence = input_sequence.split()
        for item in input_sequence:
            self.sequence.add(float(item))

        self.length = self.sequence.size()

    def first_k_elements(self, k):
        if k > self.length:
            raise ValueError

        result = type(self.sequence)()
        for i in range(k):
            result.add(self.sequence.get(i))
        return result

    def _is_increasing(self):
        for i in range(self.length - 1):
            if self.sequence.get(i) > self.sequence.get(i + 1):
                return False
        return True

    def _is_decreasing(self):
        for i in range(0, self.length - 1):
            if self.sequence.get(i) < self.sequence.get(i + 1):
                return  False

        return True


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
            return False

        return True

    def limit(self, to_inf = True):
        raise NotImplementedError("Limit is defined only for infinite sequences.")


    def partial_sum(self, n):
        if n > self.length:
            raise IndexError
        partial_sum = 0
        for i in range(n):
            partial_sum += self.sequence.get(i)

        return partial_sum
