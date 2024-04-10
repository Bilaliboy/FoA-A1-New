""""
    Array-based implementation of SortedList ADT.
    Items to store should be of time ListItem.
"""

from data_structures.referential_array import ArrayR
from data_structures.sorted_list_adt import *

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev and Graeme Gange'
__docformat__ = 'reStructuredText'

class ArraySortedList(SortedList[T]):
    """ SortedList ADT implemented with arrays. """
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int, descending=False) -> None:
        """ ArraySortedList object initialiser. """

        # first, calling the basic initialiser
        SortedList.__init__(self)

        # initialising the internal array
        size = max(self.MIN_CAPACITY, max_capacity)
        self.array = ArrayR(size)
        self.descending = descending
    
    def remove(self, item: T) -> None:
        """ Remove an item from the list. """
        index = self.index(item)
        self.delete_at_index(index)

    def reset(self):
        """ Reset the list. """
        SortedList.__init__(self)

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        return self.array[index]
    

    #changed to add descenging
    def __setitem__(self, index: int, item: ListItem) -> None:
        """
        Override the item assignment method to insert an item at a specified index,
        shifting subsequent elements to the right to maintain order. This method ensures
        that the insertion respects the sorted order of the list, whether it's ascending or descending.

        Args:
            index (int): The position at which to insert the item.
            item (ListItem): The item to insert.
        
        Time complexity:
        Best case:
        Worst case:

        Raises:
            IndexError: If attempting to insert the item would violate the list's sorted order.
        """
        # Handle the ascending order scenario
        if not self.descending:
            # Make sure the item being inserted is being inserted so that the list remains sorted
            if self.is_empty() or \
                    (index == 0 and item.key <= self[index].key) or \
                    (index == len(self) and self[index - 1].key <= item.key) or \
                    (index > 0 and self[index - 1].key <= item.key <= self[index].key):

                # If the list is full before the insertion, increase its capacity.
                if self.is_full():
                    self._resize()

                # Shift elements to the right to make room for the new item.
                self._shuffle_right(index)
                # Insert the new item at the specified index.
                self.array[index] = item
            else:
                # If the insertion would violate the sorted order, raise an error.
                raise IndexError('Element should be inserted in sorted order')

        # Handle the descending order scenario
        else:
           # Make sure the item being inserted is being inserted so that the list remains sorted
            if self.is_empty() or \
                    (index == 0 and item.key >= self[index].key) or \
                    (index == len(self) and self[index - 1].key >= item.key) or \
                    (index > 0 and self[index - 1].key >= item.key >= self[index].key):

                # If the list is full before the insertion, increase its capacity.
                if self.is_full():
                    self._resize()

                # Shift elements to the right to make room for the new item.
                self._shuffle_right(index)
                # Insert the new item at the specified index.
                self.array[index] = item
            else:
                # If the insertion would violate the sorted order, raise an error.
                raise IndexError('Element should be inserted in sorted order')


    def __contains__(self, item: ListItem):
        """ Checks if value is in the list. """
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def _shuffle_right(self, index: int) -> None:
        """ Shuffle items to the right up to a given position. """
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def _shuffle_left(self, index: int) -> None:
        """ Shuffle items starting at a given position to the left. """
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def _resize(self) -> None:
        """ Resize the list. """
        # doubling the size of our list
        new_array = ArrayR(2 * len(self.array))

        # copying the contents
        for i in range(self.length):
            new_array[i] = self.array[i]

        # referring to the new array
        self.array = new_array

    def delete_at_index(self, index: int) -> ListItem:
        """ Delete item at a given position. """
        if index >= len(self):
            raise IndexError('No such index in the list')
        item = self.array[index]
        self.length -= 1
        self._shuffle_left(index)
        return item

    def index(self, item: ListItem) -> int:
        """ Find the position of a given item in the list. """
        pos = self._index_to_add(item)
        if pos < len(self) and self[pos] == item:
            return pos
        raise ValueError('item not in list')

    def is_full(self):
        """ Check if the list is full. """
        return len(self) >= len(self.array)

    def add(self, item: ListItem) -> None:
        """ Add new element to the list. """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self._index_to_add(item)

        self[position] = item
        self.length += 1

    #changed to incorporate descending order.
    def _index_to_add(self, item: ListItem) -> int:
        """
        Find the position where the new item should be placed in the sorted list,
        taking into account whether the list is sorted in ascending or descending order.

        Time complexity:
        Best case:
        Worst case:

        Args:
            item (ListItem): The item to be added to the list.

        Returns:
            int: The index at which the new item should be inserted to maintain the sorted order.
        """

        # Initialize the lower and upper bounds of the search space
        low = 0
        high = len(self) - 1

        # Binary search to find the correct insertion index for 'item'
        while low <= high:
            # Calculate the midpoint for the current search space
            mid = (low + high) // 2

            # Case for ascending order and 'item' key is greater than 'mid' key,
            # or descending order and 'item' key is less than 'mid' key.
            # This means 'item' should be placed after 'mid', so adjust 'low' to narrow the search space.
            if (not self.descending and self[mid].key < item.key) or \
            (self.descending and self[mid].key > item.key):
                low = mid + 1

            # Case for ascending order and 'item' key is less than 'mid' key,
            # or descending order and 'item' key is greater than 'mid' key.
            # This means 'item' should be placed before 'mid', so adjust 'high' to narrow the search space.
            elif (not self.descending and self[mid].key > item.key) or \
                (self.descending and self[mid].key < item.key):
                high = mid - 1

            # If 'item' key is equal to the 'mid' key, return 'mid' as the correct insertion index.
            else:
                return mid

        # If the loop exits without finding an exact match, 'low' will be the correct insertion index.
        return low
