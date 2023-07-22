import unittest

import pytest
from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, precondition, rule
from hypothesis.strategies import integers

from order import LineItem


@given(integers(), integers())
def test_line_item(price : int, quantity : int) -> None:
    line_item = LineItem('Apple', price, quantity)
    assert line_item.total == quantity * price


 class OrderTest(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()

OrderTestCase : unittest.TestCase = OrderTest.TestCase