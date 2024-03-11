"""Assignment 1 - Grocery Store Events (Task 2)

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:

When you are done Task 2, this file should contain all the classes
necessary to model the different kinds of events in the simulation.
"""
from __future__ import annotations

from io import StringIO
from typing import TextIO
from store import GroceryStore, Customer, Item, NoAvailableLineError


class Event:
    """An event in our grocery store simulation.

    Events have an ordering based on the event timestamp. For any two events
    e1 and e2, e1 < e2 iff event e1 has a timestamp that is less than event e2.
    This signifies that e1 happens before e2.

    This is an abstract class and should not be instantiated.

    Attributes:
    - timestamp: The time when this event occurs.

    Representation Invariants:
    - timestamp >= 0
    """
    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Preconditions:
            - timestamp >= 0

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following three methods allow for comparison of Event instances
    # using the standard comparison operators, such as ==, <, and <=.
    # All methods simply perform the desired comparison on the 'timestamp'
    # attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return whether this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def do(self, store: GroceryStore) -> list[Event]:
        """Perform this event as specified in the A1 handout, and return any
        events generated by doing so.
        """
        raise NotImplementedError


class CustomerArrival(Event):
    """A customer arrives at the checkout area ready to join a line and
    check out.

    Attributes:
    - customer: The arriving customer
    """
    timestamp: int
    customer: Customer

    def __init__(self, timestamp: int, c: Customer) -> None:
        """Initialize a CustomerArrival event with the given <timestamp>
        and customer <c>.

        If the customer's arrival time is None, set it now to record
        the fact that this is the time when they first arrived at the
        checkout area. (This is the start of their waiting time.)

        Preconditions:
        - timestamp >= 0
        """
        Event.__init__(self, timestamp)
        self.customer = c

    def do(self, store: GroceryStore) -> list[Event]:
        """Complete a CustomerArrival event, where a customer arrives at the
        checkout area. A customer joins the line with the lowest amount of
        customers or the lowest index if it's a tie. Otherwise, the customer
        arrives at a later timestamp.
        """
        # find the smallest line or smallest with lowest index
        # if line is found, add timestamp to customer arrival and enter line
        # if no line is available, raise NoAvailableLineError
        smallest_line_index = None
        smallest_line_size = float('inf')

        for i in range(len(store.checkout_lines)):
            line = store.checkout_lines[i]
            if (line.can_accept(self.customer) and line.is_open
                    and len(line) < smallest_line_size):
                smallest_line_size = len(line)
                smallest_line_index = i

        if smallest_line_index is not None:
            smallest_line = store.checkout_lines[smallest_line_index]
            smallest_line.accept(self.customer)
            if smallest_line.first_in_line() == self.customer:
                return [CheckoutStarted(self.timestamp, smallest_line_index)]

        if smallest_line_index is None:
            CustomerArrival(self.timestamp + 1, self.customer).do(store)
            raise NoAvailableLineError
        # TODO: Not sure if correct, especially process of creating new event

        return []


class CheckoutStarted(Event):
    """A customer starts the checkout process in a particular checkout line.

    Attributes:
    - line_number: The number of the checkout line.
    """
    timestamp: int
    line_number: int

    def __init__(self, timestamp: int, line_number: int) -> None:
        """Initialize a CheckoutStarted event with the given <timestamp>
        and <line_number>.

        Preconditions:
        - timestamp >= 0
        - line_number >= 0
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number

    def do(self, store: GroceryStore) -> list[Event]:
        """A customer has reached the front of a particular line, and the
        checkout process begins for all of their items."""
        checkout_time = store.checkout_lines[self.line_number].\
            next_checkout_time()
        completion_timestamp = self.timestamp + checkout_time
        customer = store.first_in_line()
        return [CheckoutCompleted(completion_timestamp, self.line_number,
                                  customer)]

        # TODO: Check if this works


class CheckoutCompleted(Event):
    """A customer finishes the checkout process.

    Attributes:
    - line_number: The number of the checkout line where a customer
      is finishing.
    - customer: The finishing customer.
    """
    timestamp: int
    line_number: int
    customer: Customer

    def __init__(self, timestamp: int, line_number: int, c: Customer) -> None:
        """Initialize a CheckoutCompleted event.
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number
        self.customer = c

    def do(self, store: GroceryStore) -> list[Event]:
        """A customer finishes the checkout process and leaves the checkout line
        they are in."""
        store.checkout_lines[self.line_number].remove_front_customer()
        if store.checkout_lines[self.line_number].first_in_line() is not None:
            return [CheckoutStarted(self.timestamp, self.line_number)]
        return []

        # TODO: Check if this works too


class CloseLine(Event):
    """A CheckoutLine gets closed.

    Attributes:
    - line_number: The number of the checkout line.
    """
    timestamp: int
    line_number: int

    def __init__(self, timestamp: int, line_number: int) -> None:
        """Initialize a CloseLine event.
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number

    def do(self, store: GroceryStore) -> list[Event]:
        """All customers in the specified line must join a new line except
        the first customer in line."""
        removed_customers = store.close_line(self.line_number)
        events = []
        for customer in removed_customers:
            new_line_index = -1
            smallest_line_size = float('inf')
            for i in range(len(store.checkout_lines)):
                line = store.checkout_lines[i]
                if line.can_accept(customer) and len(line) < smallest_line_size:
                    smallest_line_size = len(line)
                    new_line_index = i
            if new_line_index >= 0:
                new_line = store.checkout_lines[new_line_index]
                new_line.accept(customer)
                if new_line.first_in_line() == customer:
                    events.append(CheckoutStarted(self.timestamp,
                                                  new_line_index))
        return events

        # TODO: Check if this is correct


EVENT_SAMPLE = StringIO("""121 Arrive William Bananas 7
22 Arrive Trevor Flowers 22 Bread 3 Cheese 3 Cheese 3
41 Close 0""")


def create_event_list(event_file: TextIO) -> list[Event]:
    """Return a list of Event objects to represent the events in <filename>.

    The events in the list must be in the same order as they are in the file.

    Preconditions:
    - <event_file> is open.
    - <event_file> is in the format specified by the assignment handout.

    >>> samp_events = create_event_list(EVENT_SAMPLE)
    >>> len(samp_events) == 3
    True
    >>> isinstance(samp_events[0], CustomerArrival)
    True
    >>> isinstance(samp_events[2], CloseLine)
    True
    """
    data = event_file.readlines()
    output = []

    for i in data:
        split_string = i.split()
        items = []

        if split_string[1] == 'Arrive':
            for j in range(0, len(split_string[3:]) - 1, 2):
                items.append(Item(str(j), j + 1))

            customer = Customer(split_string[2], items)
            event = CustomerArrival(int(split_string[0]), customer)
            output.append(event)
        else:
            output.append(CloseLine(int(split_string[0]), len(split_string[2])))

    return output


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing', 'store',
                                       'python_ta', 'doctest', 'io']})
