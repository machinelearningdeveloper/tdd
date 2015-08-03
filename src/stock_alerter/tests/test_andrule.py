import arrow
import unittest
from ..stock import Stock
from ..rule import AndRule, PriceRule

class AndRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(klass):
        goog = Stock('GOOG')
        goog.update(arrow.get(2014, 2, 10), 8)
        goog.update(arrow.get(2014, 2, 11), 10)
        goog.update(arrow.get(2014, 2, 12), 12)
        msft = Stock('MSFT')
        msft.update(arrow.get(2014, 2, 10), 10)
        msft.update(arrow.get(2014, 2, 11), 10)
        msft.update(arrow.get(2014, 2, 12), 12)
        redhat = Stock('RHT')
        redhat.update(arrow.get(2014, 2, 10), 7)
        klass.exchange = {'GOOG': goog, 'MSFT': msft, 'RHT':redhat}

    def test_an_AndRule_matches_if_all_component_rules_are_true(self):
        rule = AndRule(PriceRule('GOOG', lambda stock: stock.price > 8), PriceRule('MSFT', lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))

    def test_an_AndRule_does_not_match_if_at_least_one_component_rule_does_not_match(self):
        rule = AndRule(PriceRule('GOOG', lambda stock: stock.price > 8), PriceRule('MSFT', lambda stock: stock.price < 10))
        self.assertFalse(rule.matches(self.exchange))

    def test_an_AndRule_does_not_match_if_a_Stock_is_not_in_the_exchange(self):
        rule = AndRule(PriceRule('GOOG', lambda stock: stock.price > 8), PriceRule('AAPL', lambda stock: stock.price > 10))
        self.assertFalse(rule.matches(self.exchange))