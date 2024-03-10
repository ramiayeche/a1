"""Assignment 1 - Tests for class PriorityQueue  (Task 3a)

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module will contain tests for class PriorityQueue.
"""
from container import PriorityQueue


class TestPriorityQueue:
    """A set of Tester cases that provide full coverage of the PriorityQueue
    Class."""

    def test_init(self):
        """Test the initializer method of the PriorityQueue class. Check if
        the instance attributes are correctly initialized."""
        queue = PriorityQueue()
        assert queue.is_empty()

    def test_remove_basic(self):
        """Test the remove() method of the PriorityQueue class through a basic
        set of elements, and remove the one with highest priority."""
        queue = PriorityQueue()
        queue.add('Rami')
        queue.add('Shah')
        queue.add(13)
        queue.add(22.3)
        queue.remove()
        assert queue._items == [22.3, 'Rami', 'Shah']

    def test_remove_mixed(self):
        """More complex test of remove() from PriorityQueue, add a set of mixed
        data types and test if the remove() method returns the correct type"""
        queue = PriorityQueue()
        queue.add(29)
        queue.add(11)
        queue.add(15.3)
        queue.add(True)
        queue.add((2, 4))
        queue.add('Fred')
        queue.add('Gilbert')
        queue.remove()
        queue.remove()
        assert queue.remove() == (2, 4)

    def test_is_empty(self):
        """Test is_empty() from PriorityQueue through adding and removing
        elements until the queue is empty, and check using is_empty()."""
        queue = PriorityQueue()
        queue.add('Anna')
        queue.add(13)
        queue.remove()
        queue.remove()
        assert queue.is_empty()

    def test_add_basic(self):
        """Basic test of the functionality of add() in PriorityQueue"""
        queue = PriorityQueue()
        queue.add('Ben')
        queue.add(2)
        assert queue._items == [2, 'Ben']

    def test_add_complex(self):
        """More complex testing of add() by using mixed data types in the
        PriorityQueue"""
        queue = PriorityQueue()
        queue.add('Rami')
        queue.add(False)
        queue.add(17)
        queue.add('John')
        assert queue._items == [False, 17, 'John', 'Rami']


if __name__ == '__main__':
    import pytest

    pytest.main(['test_priority_queue.py'])
