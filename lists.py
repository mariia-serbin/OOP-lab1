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
        swap(el1, el2): Swaps two items of list.

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

    @abstractmethod
    def swap(self, index1, index2):
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
            raise IndexError('Index is out of appropriate range.')

    def _get_element(self, value):
        for i in range(self.size):
            if self._data[i] == value:
                return i

    def set(self, index, value):
        if 0 <= index < self._count:
            self._data[index] = value
        else:
            pass
    @property
    def size(self):
        return self._count

    def swap(self, value1, value2):
        index1 = self._get_element(value1)
        index2 = self._get_element(value2)
        self.set(index1, value2)
        self.set(index2, value1)


# implementation of linked lists

class Node:
    """
    Node is a class for a node for linked lists.
    Attributes:
        data: stores data of the node.
        next: stores pointer to the next node.
    """

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList(BaseList):
    """
    LinkedList is a class for linked lists.
    Attributes:
        head: stores head(start) of the linked list.
    Methods:
        add(item): Adds a new item to the end of the linked list.
        remove(item): Removes item from the linked list.
        get(index): Returns the item at the given index.
        set(index, value): Sets the new value to the node in given position(index).
        size(): Returns the number of items in the linked list.
    """

    def __init__(self):
        self.head = None

    def add(self, item):
        node = Node(item)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def remove(self, index):
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        current.next = current.next.next

    def get(self, index):
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        return current.data

    def set(self, index, value):
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        current.data = value

    def swap(self, el1, el2):
        el1.data, el2.data = el2.data, el1.data

    @property
    def size(self):
        size = 0
        current = self.head
        while current.next:
            current = current.next
            size += 1
        return size


# implementation of doubly linked list

class DoublyNode(Node):
    """
    DoublyNode is a class for a node of doubly linked list.
    Attributes:
        data: stores data of node
        next: stores pointer to the next element
        prev: stores pointer to the previous element
    """

    def __init__(self, data):
        super().__init__(data)
        self.prev = None


class DoublyLinkedList(LinkedList):
    """
    DoublyLinkedList is a class for doubly linked list.
    Attributes:
        head: stores head(start) of the doubly linked list.
        tail: stores tail(end) of the doubly linked list.
    Methods:
        size(): Returns the number of elements in the doubly linked list.
        add(item): Adds a new item to the doubly linked list.
        remove(item): Removes item from the doubly linked list.
        find_node_by_index(index): Returns the node at the given index.
        get(index): returns value of element at given index.
        set(index, value): Sets the new value to the node in given position(index).
    """

    def __init__(self):
        super().__init__()
        self.tail = None

    @property
    def size(self):
        size = 0
        current = self.head
        while current.next:
            current = current.next
            size += 1
        return size

    def add(self, item):
        node = DoublyNode(item)
        if self.head is None:
            self.head = self.tail = node

        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def remove(self, index):
        if self.head is None:
            return

        current = self.head
        i = 0
        if index == 0:
            self.head = current.next
            if self.head:
                self.head.prev = None
            return

        while current.next and i < index:
            current = current.next
            i += 1

        if i != index:
            raise IndexError("Index out of range")

        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev

    def find_node_by_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        if index < self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - 1, index, -1):
                current = current.prev
        return current

    def get(self, index):
        node = self.find_node_by_index(index)
        return node.data

    def set(self, index, value):
        node = self.find_node_by_index(index)
        node.data = value

    def swap(self, el1, el2):
        el1.data, el2.data = el2.data, el1.data
