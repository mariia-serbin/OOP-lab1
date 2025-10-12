from abc import *

#base list (abstract class)
class BaseList(ABC):

    """
    Base class for all lists.
    Methods:
        add(item): Adds a new item to the list to the end of the list.
        remove(item): Removes item from the list.
        get(index): Returns the item at the given index.
        set(index): Sets the index of the item to the given value.
        size(): Returns the number of items in the list.

    """
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self, index):
        pass

    @abstractmethod
    def get(self, index):
        pass

    @abstractmethod
    def set(self,index, value):
        pass

    @abstractmethod
    def size(self):
        pass

#list based on array

class ArrayList(BaseList):

    """
    ArrayList is a class for lists based on arrays.
    Attributes:
        _data: stores data of the list.
        capacity: stores number of elements the list can store .
        _count: stores number of elements in the list.
    Methods:
        _resize(): Resizes the list (changes the capacity of the list).
        add(item): Adds a new item to the list to the end of the list.
        remove(item): Removes item from the list by the given index.
        get(index): Returns the item at the given index.
        set(index): Sets the index of the item to the given value.
        size(): Returns the number of items in the list.

    """

    def __init__(self, size = 10):
        self._data = [None] * size
        self.capacity = size
        self._count = 0
    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self._count):
            new_data[i] = self._data[i]

        self._data = new_data
        del new_data

    def add(self, item):
        if self._count == self.capacity:
            self._resize()
        self._data[self._count] = item
        self._count += 1

    def remove(self, index):
        if 0 <= index < self._count:
            for i in range(index, self._count - 1):
                self._data[i] = self._data[i + 1]
            self._data[self._count - 1] = None
            self._count -= 1
        else:
            raise IndexError("Index is out of appropriate range.")

    def get(self, index):
        if 0 <= index < self._count:
            return self._data[index]
        else:
            pass

    def set(self, index, value):
        if 0 <= index < self._count:
            self._data[index] = value
        else:
            pass
    @property
    def size(self):
        return self._count
