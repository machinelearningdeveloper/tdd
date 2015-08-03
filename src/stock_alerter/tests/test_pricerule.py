import arrow
import unittest
from ..stock import Stock
from ..rule import PriceRule

class PriceRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(klass):
        goog = Stock('GOOG')
        goog.update(arrow.get(2014, 2, 10), 11)
        klass.exchange = {'GOOG': goog}

    def test_a_PriceRule_matches_when_Stock_meets_condition(self):
        rule = PriceRule('GOOG', lambda stock: stock.price > 10)
        self.assertTrue(rule.matches(self.exchange))

    def test_a_PriceRule_does_not_match_when_Stock_does_not_meet_condition(self):
        rule = PriceRule('GOOG', lambda stock: stock.price < 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_does_not_match_Stock_not_in_exchange(self):
        rule = PriceRule('MSFT', lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_does_not_match_new_Stock(self):
        self.exchange['AAPL'] = Stock('AAPL')
        rule = PriceRule('AAPL', lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_only_depends_on_its_Stock(self):
        rule = PriceRule('MSFT', lambda stock: stock.price > 10)
        self.assertEqual({'MSFT'}, rule.depends_on())