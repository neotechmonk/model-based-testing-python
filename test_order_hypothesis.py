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

    @precondition(lambda self : len(self.line_items)> 0) 
    @rule(data = st.data())
    def add_line_line_to_order(self, data : st.SearchStrategy) -> None: 
        line_item = data.draw(st.sampled_from(self.line_items))
        self.order.add_line_item(line_item)

    @precondition(lambda self : len(self.order.line_items)> 0) 
    @rule(data = st.data())
    def remove_line_litem_from_order(self, data : st.SearchStrategy) -> None: 
        line_item = data.draw(st.sampled_from(self.order.line_items))
        self.order.remove_line_item(line_item)
    

    @precondition(lambda self : len(self.order.line_items)== 0 and len(self.line_items)> 0) 
    @rule(data = st.data())
    def remove_a_non_existing_line_litem_from_order(self, data : st.SearchStrategy) -> None: 
        line_item = data.draw(st.sampled_from(self.line_items))
        with pytest.raises(ValueError) : 
            self.order.remove_line_item(line_item)


    @rule()
    def total_agrees(self) -> None:
        assert sum(li.total for li in self.order.line_items) == self.order.total

OrderTestCase : unittest.TestCase = OrderTest.TestCase