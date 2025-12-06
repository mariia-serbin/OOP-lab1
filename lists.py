"""!
@file lists.py
@brief List data structures module.
@details Contains abstract base class for lists (BaseList) and implementations based on arrays (ArrayList),
         singly linked lists (LinkedList), doubly linked lists (DoublyLinkedList), and Python built-in lists
         (LibraryList). Provides all basic operations including addition, removal, retrieval, setting, swapping,
         and computation of maximum and minimum values. Handles exceptions for invalid indices and empty structures.
@author
Maria Serbin
@date
06.12.2025
"""

from abc import *

#base list (abstract class)
class BaseList(ABC):
    """!
        @brief Abstract base class for all types of lists.

        @details Provides an interface for all list types. Any subclass must implement the following methods:
                 add, remove, get, set, size, swap, max, min. Ensures a uniform API for different list implementations.
    """
    @abstractmethod
    def add(self, item):
        """!
                @brief Adds an item to the list.
                @param item The item to be added.
        """
        pass

    @abstractmethod
    def remove(self, index):
        """!
        @brief Removes an item from the list by index.
        @param index The index of the item to remove.
        @throws IndexError If the index is out of range.
        """
        pass

    @abstractmethod
    def get(self, index):
        """!
        @brief Returns the item at the given index.
        @param index Index of the item.
        @return The item at the specified index.
        @throws IndexError If the index is out of range.
        """
        pass

    @abstractmethod
    def set(self,index, value):

        """!
        @brief Sets the item at a given index to a new value.
        @param index Index of the item to set.
        @param value New value to store at the index.
        @throws IndexError If the index is out of range.
        """
        pass

    @abstractmethod
    def size(self):

        """!
        @brief Returns the number of items in the list.
        @return Number of items in the list.
        """
        pass

    @abstractmethod
    def swap(self, index1, index2):
        """!
        @brief Swaps two items in the list.
        @param index1 Index of the first item.
        @param index2 Index of the second item.
        @throws IndexError If any index is out of range.
        """
        pass

    @abstractmethod
    def max(self):

        """!
        @brief Returns the largest numeric item in the list.
        @return The maximum numeric value in the list.
        @throws ValueError If the list has no numeric elements.
        """
        pass

    @abstractmethod
    def min(self):
        """!
        @brief Returns the smallest numeric item in the list.
        @return The minimum numeric value in the list.
        @throws ValueError If the list has no numeric elements.
        """
        pass
#list based on array

class ArrayList(BaseList):
    """!
    @brief List implementation based on arrays.

    @details Stores elements in a contiguous array and supports automatic resizing.
             Provides standard list operations, as well as finding maximum and minimum numeric values.
    """

    def __init__(self, size = 10):
        self._data = [None] * size
        self.capacity = size
        self._count = 0

    def __iter__(self):
        for i in range(self._count):
            yield self._data[i]

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self._count):
            new_data[i] = self._data[i]

        self._data = new_data
        del new_data

    def add(self, item):
        """!
        @brief Adds a new item to the end of the array list.
        @param item The item to add.
        @details Automatically resizes the underlying array if capacity is exceeded.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(5)
        print(lst.get(0))  # 5
        @endcode
        """
        if self._count == self.capacity:
            self._resize()
        self._data[self._count] = item
        self._count += 1

    def remove(self, index):

        """!
        @brief Removes an item at the given index.
        @param index Index of the item to remove.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(1)
        lst.add(2)
        lst.remove(0)
        print(lst.get(0))  # 2
        @endcode
        """
        if 0 <= index < self._count:
            for i in range(index, self._count - 1):
                self._data[i] = self._data[i + 1]
            self._data[self._count - 1] = None
            self._count -= 1
        else:
            raise IndexError("Index is out of appropriate range.")

    def get(self, index):

        """!
        @brief Returns the item at the specified index.
        @param index Index of the item.
        @return The item stored at the given index.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(10)
        print(lst.get(0))  # 10
        @endcode
        """
        if 0 <= index < self._count:
            return self._data[index]
        else:
            raise IndexError('Index is out of appropriate range.')

    def _get_element(self, value):
        for i in range(self.size):
            if self._data[i] == value:
                return i
        return None


    def set(self, index, value):

        """!
        @brief Sets a new value at the specified index.
        @param index Index of the item.
        @param value New value to set.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(5)
        lst.set(0, 10)
        print(lst.get(0))  # 10
        @endcode
        """
        if 0 <= index < self._count:
            self._data[index] = value
        else:
            pass
    @property
    def size(self):

        """!
        @brief Returns the number of items in the array list.
        @return Number of items in the list.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(1)
        print(lst.size)  # 1
        @endcode
        """
        return self._count

    def swap(self, value1, value2):

        """!
        @brief Swaps two items in the array list by their values.
        @param value1 First value to swap.
        @param value2 Second value to swap.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(1)
        lst.add(2)
        lst.swap(1, 2)
        print(lst.get(0))  # 2
        print(lst.get(1))  # 1
        @endcode
        """
        index1 = self._get_element(value1)
        index2 = self._get_element(value2)
        self.set(index1, value2)
        self.set(index2, value1)

    def max(self):

        """!
        @brief Returns the largest numeric value in the array list.
        @return Maximum numeric value.
        @throws ValueError If no numeric elements exist.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(3)
        lst.add(7)
        print(lst.max())  # 7
        @endcode
        """
        max_value = float('-inf')
        for el in self._data[:self._count]:
            if isinstance(el, (int, float)) and el > max_value:
                max_value = el
        if max_value == float('-inf'):
            raise ValueError("No numeric elements in ArrayList")
        return max_value

    def min(self):
        """!
        @brief Returns the smallest numeric value in the array list.
        @return Minimum numeric value.
        @throws ValueError If no numeric elements exist.
        @par Example:
        @code
        lst = ArrayList()
        lst.add(3)
        lst.add(7)
        print(lst.min())  # 3
        @endcode
        """
        min_value = float('inf')
        for el in self._data[:self._count]:
            if isinstance(el, (int, float)) and el < min_value:
                min_value = el
        if min_value == float('inf'):
            raise ValueError("No numeric elements in ArrayList")
        return min_value


# implementation of linked lists

class Node:
    """!
    @brief Node class for linked lists.
    @details Represents a single node in a linked list. Each node stores data and a pointer to the next node.
    """

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList(BaseList):
    """!
    @brief Singly linked list implementation.
    @details Stores elements in nodes linked sequentially. Supports standard list operations
             such as adding, removing, getting, setting, swapping elements, and computing
             maximum and minimum numeric values.
    """

    def __init__(self):
        self.head = None

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def add(self, item):

        """!
        @brief Adds a new item to the end of the linked list.
        @param item The value to add.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(5)
        print(lst.get(0))  # 5
        @endcode
        """
        node = Node(item)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def remove(self, index):

        """!
        @brief Removes an item at the specified index.
        @param index Index of the item to remove.
        @throws IndexError If the index is out of range or list is empty.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(1)
        lst.add(2)
        lst.remove(0)
        print(lst.get(0))  # 2
        @endcode
        """
        if self.size < index or index < 0 or not self.head:
            raise IndexError('Index is out of appropriate range.')
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        current.next = current.next.next

    def get(self, index):

        """!
        @brief Returns the item at the specified index.
        @param index Index of the item to retrieve.
        @return The value at the given index.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(10)
        print(lst.get(0))  # 10
        @endcode
        """
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        return current.data

    def set(self, index, value):

        """!
        @brief Sets a new value at the specified index.
        @param index Index of the item to set.
        @param value New value to store.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(5)
        lst.set(0, 15)
        print(lst.get(0))  # 15
        @endcode
        """
        i = 0
        current = self.head
        while current.next and i < index:
            current = current.next
            i += 1
        current.data = value

    def swap(self, index1, index2):

        """!
        @brief Swaps two items in the linked list.
        @param index1 Index of the first item.
        @param index2 Index of the second item.
        @throws IndexError If any index is out of range.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(1)
        lst.add(2)
        lst.swap(0, 1)
        print(lst.get(0))  # 2
        print(lst.get(1))  # 1
        @endcode
        """
        if index1 == index2:
            return
        node1 = self.head
        for _ in range(index1):
            node1 = node1.next
        node2 = self.head
        for _ in range(index2):
            node2 = node2.next
        node1.data, node2.data = node2.data, node1.data

    @property
    def size(self):

        """!
        @brief Returns the number of items in the linked list.
        @return Number of items.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(1)
        print(lst.size)  # 1
        @endcode
        """
        size = 0
        current = self.head
        while current:
            current = current.next
            size += 1
        return size

    def max(self):

        """!
        @brief Returns the largest value in the linked list.
        @return Maximum value.
        @throws IndexError If the list is empty.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(3)
        lst.add(7)
        print(lst.max())  # 7
        @endcode
        """
        if not self.head:
            raise IndexError("Linked list is empty.")

        max_value = self.head.data
        current = self.head.next
        while current:
            if current.data > max_value:
                max_value = current.data
            current = current.next

        return max_value

    def min(self):
        """!
        @brief Returns the smallest value in the linked list.
        @return Minimum value.
        @throws IndexError If the list is empty.
        @par Example:
        @code
        lst = LinkedList()
        lst.add(3)
        lst.add(7)
        print(lst.min())  # 3
        @endcode
        """

        if not self.head:
            raise IndexError("Linked list is empty.")

        min_value = self.head.data
        current = self.head.next
        while current:
            if current.data < min_value:
                min_value = current.data
            current = current.next

        return min_value


# implementation of doubly linked list

class DoublyNode(Node):

    """!
    @brief Node class for doubly linked lists.
    @details Extends the Node class by adding a pointer to the previous node.
             Each node stores data, a next pointer, and a previous pointer.
    """
    def __init__(self, data):
        super().__init__(data)
        self.prev = None

class DoublyLinkedList(LinkedList):
    """!
    @brief Doubly linked list implementation.
    @details Stores elements in nodes linked both forward and backward. Supports standard list operations
             such as adding, removing, getting, setting, swapping elements, and computing
             maximum and minimum numeric values.
    """

    def __init__(self):
        super().__init__()
        self.tail = None

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    @property
    def size(self):
        """!
        @brief Returns the number of elements in the doubly linked list.
        @return Number of elements.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(1)
        print(lst.size)  # 1
        @endcode
        """
        size = 0
        current = self.head
        while current:
            current = current.next
            size += 1
        return size

    def add(self, item):
        """!
        @brief Adds a new item to the end of the doubly linked list.
        @param item The value to add.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(5)
        print(lst.get(0))  # 5
        @endcode
        """
        node = DoublyNode(item)
        if self.head is None:
            self.head = self.tail = node

        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def remove(self, index):
        """!
        @brief Removes an item at the specified index.
        @param index Index of the item to remove.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(1)
        lst.add(2)
        lst.remove(0)
        print(lst.get(0))  # 2
        @endcode
        """
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

    def _find_node_by_index(self, index):
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

        """!
        @brief Returns the value of the element at the given index.
        @param index Index of the element.
        @return Value at the index.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(10)
        print(lst.get(0))  # 10
        @endcode
        """
        node = self._find_node_by_index(index)
        return node.data

    def set(self, index, value):

        """!
        @brief Sets a new value at the specified index.
        @param index Index of the element.
        @param value New value to store.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(5)
        lst.set(0, 20)
        print(lst.get(0))  # 20
        @endcode
        """
        node = self._find_node_by_index(index)
        node.data = value

    def swap(self, index1, index2):
        """!
        @brief Swaps two elements in the doubly linked list.
        @param index1 Index of the first element.
        @param index2 Index of the second element.
        @throws IndexError If any index is out of range.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(1)
        lst.add(2)
        lst.swap(0, 1)
        print(lst.get(0))  # 2
        print(lst.get(1))  # 1
        @endcode
        """
        if index1 == index2:
            return
        node1 = self._find_node_by_index(index1)
        node2 = self._find_node_by_index(index2)
        node1.data, node2.data = node2.data, node1.data

    def max(self):
        """!
        @brief Returns the largest value in the doubly linked list.
        @return Maximum value.
        @throws IndexError If the list is empty.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(3)
        lst.add(7)
        print(lst.max())  # 7
        @endcode
        """
        if not self.head:
            raise IndexError("Linked list is empty.")

        max_value = self.head.data
        current = self.head.next
        while current:
            if current.data > max_value:
                max_value = current.data
            current = current.next

        return max_value

    def min(self):
        """!
        @brief Returns the smallest value in the doubly linked list.
        @return Minimum value.
        @throws IndexError If the list is empty.
        @par Example:
        @code
        lst = DoublyLinkedList()
        lst.add(3)
        lst.add(7)
        print(lst.min())  # 3
        @endcode
        """
        if not self.head:
            raise IndexError("Linked list is empty.")
        min_value = self.head.data
        current = self.head.next
        while current:
            current = current.next
            if current.data < min_value:
                min_value = current.data

        return min_value

class LibraryList(BaseList):

    """!
    @brief List implementation using Python's built-in list.
    @details Provides standard list operations such as adding, removing, getting, setting, swapping elements,
             and computing maximum and minimum values. Internally uses a Python list to store elements.
    """
    def __init__(self):
        self._data = []
    def add(self, item):
        """!
        @brief Adds a new item to the end of the list.
        @param item The value to add.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(5)
        print(lst.get(0))  # 5
        @endcode
        """
        self._data.append(item)

    def remove(self, index):
        """!
        @brief Removes an item at the specified index.
        @param index Index of the item to remove.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(1)
        lst.add(2)
        lst.remove(0)
        print(lst.get(0))  # 2
        @endcode
        """
        if index < 0 or index >= len(self._data):
            self._data.pop(index)
        else:
            raise IndexError("Index out of range")

    def get(self, index):
        """!
        @brief Returns the item at the specified index.
        @param index Index of the item.
        @return Value at the given index.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(10)
        print(lst.get(0))  # 10
        @endcode
        """
        return self._data[index]

    def set(self, index, value):
        """!
        @brief Sets a new value at the specified index.
        @param index Index of the item.
        @param value New value to store.
        @throws IndexError If the index is out of range.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(5)
        lst.set(0, 20)
        print(lst.get(0))  # 20
        @endcode
        """
        self._data[index] = value

    def size(self):
        """!
        @brief Returns the number of items in the list.
        @return Number of items.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(1)
        print(lst.size())  # 1
        @endcode
        """
        return len(self._data)

    def swap(self, index1, index2):
        """!
        @brief Swaps two items in the list.
        @param index1 Index of the first item.
        @param index2 Index of the second item.
        @throws IndexError If any index is out of range.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(1)
        lst.add(2)
        lst.swap(0, 1)
        print(lst.get(0))  # 2
        print(lst.get(1))  # 1
        @endcode
        """
        self._data[index1], self._data[index2] = self._data[index2], self._data[index1]

    def max(self):
        """!
        @brief Returns the largest value in the list.
        @return Maximum value.
        @throws ValueError If the list is empty.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(3)
        lst.add(7)
        print(lst.max())  # 7
        @endcode
        """
        data = self._data
        return max(data)

    def min(self):
        """!
        @brief Returns the smallest value in the list.
        @return Minimum value.
        @throws ValueError If the list is empty.
        @par Example:
        @code
        lst = LibraryList()
        lst.add(3)
        lst.add(7)
        print(lst.min())  # 3
        @endcode
        """
        data = self._data
        return min(data)
