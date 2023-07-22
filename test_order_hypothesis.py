import unittest

import hypothesis.strategies as st
import pytest
from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, precondition, rule

from order import LineItem, Order


@given(st.integers(), st.integers())
def test_line_item(price : int, quantity : int) -> None:
    line_item = LineItem('Apple', price, quantity)
    assert line_item.total == quantity * price


class OrderTest(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.order = Order("John Doe")
        self.line_items : list[LineItem]  = [] 
    
    @rule(description = st.text(), price = st.integers(), quantity = st.integers())
    def create_line_item(self, description : str, price : int, quantity : int)-> None: 
        self.line_items.append(LineItem(description, price, quantity))
                               

OrderTestCase : unittest.TestCase = OrderTest.TestCase