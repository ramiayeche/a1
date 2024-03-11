"""Assignment 1 - Grocery Store Simulation (Task 4)

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

This file drives a simulation of customers checking out at a grocery store.
"""
from __future__ import annotations

from typing import TextIO
from event import Event, create_event_list, CustomerArrival, CheckoutCompleted
from store import GroceryStore
from container import PriorityQueue


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    Attributes:
    - _events: A sequence of events arranged in priority order determined by
            the event comparison methods. For any two events e1 and e2,
            if e1 < e2 then e1 will come out of the event queue before e2.
            If e1 == e2 (according to the event comparison defined by __eq__),
            then the event that was inserted *earlier* is the first one to be
            removed.
    - _store: The store being simulated.
    - stats: Summary statistics for the simulation, with these keys and values:
            'num_customers': the total number of customers in the simulation
            'total_time': the timestamp of the last event
            'max_wait': the maximum amount of time a customer waited
      All statistics begin at 0 and are updated as each event is handled.

    Representation Invariants:
    - For every event in self._events that involves a checkout line number n,
      0 <= n <= self._store.num_lines.
    """
    _events: PriorityQueue
    _store: GroceryStore
    stats: dict[str, int]

    def __init__(self, store_file: TextIO) -> None:
        """Initialize a GroceryStoreSimulation using the store information in
        <store_file>.

        All statistics begin at 0.

        Preconditions:
        - store_file is a valid JSON configuration file with the keys
          regular_count, express_count, self_serve_count, and line_capacity
        - store_file is open
        - All values in store_file are >= 0
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)
        self.stats = {'num_customers': 0, 'total_time': 0, 'max_wait': 0}

    def run(self, initial_events: list[Event]) -> None:
        """Run the simulation on the events stored in <initial_events>.

        Reset the statistics for the simulation before the simulation is run.

        Precondition:
        - For every event in initial_events that involves a checkout line
          number n, 0 <= n <= self._store.num_lines.
        - initial_events does not include two CustomerArrival events a1 and a2
          such that a1.customer.name == a2.customer.name
        - The events in initial_events are such that the simulation will
          eventually end. For example, the checkout lines will not all be
          made to close when there are remaining customers.
        """
        self.stats = {'num_customers': 0, 'total_time': 0, 'max_wait': 0}

        for event in initial_events:
            self._events.add(event)

        while not self._events.is_empty():
            event = self._events.remove()
            events_to_add = event.do(self._store)
            self._update_statistics(event)

            for new_event in events_to_add:
                self._events.add(new_event)

    def _update_statistics(self, event: Event) -> None:
        """Update simulation statistics."""
        if isinstance(event, CustomerArrival):
            self.stats['num_customers'] += 1
        elif isinstance(event, CheckoutCompleted):
            wait_time = event.timestamp - event.customer.arrival_time
            if wait_time > self.stats['max_wait']:
                self.stats['max_wait'] = wait_time
        self.stats['total_time'] = event.timestamp


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    config_file_name = 'input_files/config_111_10.json'
    with open(config_file_name) as config_file:
        sim = GroceryStoreSimulation(config_file)
        config_file.close()

    # By using "with ... as ...", we get Python to automatically close the
    # file for us at the end of the "with" clause.
    event_file_name = 'input_files/events_mixtures.txt'
    with open(event_file_name) as event_file:
        events = create_event_list(event_file)
    sim.run(events)
    print(sim.stats)

    import doctest
    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta
        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing', 'event', 'store',
                                       'container', 'python_ta', 'doctest']})
