"""Assignment 1 - Grocery Store Simulation

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module contains some starter tests for Assignment 1.
You may add additional tests here, but you will not hand in this file.
"""
from io import StringIO
from simulation import GroceryStoreSimulation
from event import CustomerArrival, create_event_list
from store import GroceryStore, Customer, Item
from store import RegularLine, ExpressLine, SelfServeLine


CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
'''


# a provided sample test for the whole simulation
def test_simulation() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


CONFIG_FILE_2 = '''{
  "regular_count": 0,
  "express_count": 1,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''


def test_simulation_express() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_2))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


CONFIG_FILE_3 = '''{
  "regular_count": 0,
  "express_count": 0,
  "self_serve_count": 1,
  "line_capacity": 1
}
'''


def test_simulation_self_serve() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_3))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 31, 'max_wait': 21}


CONFIG_FILE_CLOSE = '''{
  "regular_count": 2,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE_CLOSE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
0 Close 0
'''


def test_simulation_close() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_CLOSE))
    gss.run(create_event_list(StringIO(EVENT_FILE_CLOSE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


if __name__ == '__main__':
    import pytest

    pytest.main(['test_a1.py'])
