import arrow
import unittest
from ..stock import Stock

class StockTest(unittest.TestCase):
    def setUp(self):
        self.goog = Stock('GOOG')

    def given_a_series_of_prices(self, prices):
        timestamps = [arrow.get(2014, 2, 11).replace(days=offset) for offset in range(len(prices))]
        for timestamp, price in zip(timestamps, prices):
            self.goog.update(timestamp, price)

    def test_price_of_a_new_stock_should_be_None(self):
        self.assertIsNone(self.goog.price)

    def test_stock_update(self):
        """An update should set the price on the stock object.
        We will be using the arrow module for the timestamp.
        """
        self.goog.update(arrow.get('2014-02-12'), price=10)
        self.assertEqual(10, self.goog.price)

    def test_negative_price_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            self.goog.update(arrow.get('2014-02-13'), -1)

    def test_stock_price_should_give_the_latest_price(self):
        self.goog.update(arrow.get('2014-02-12'), price=10)
        self.goog.update(arrow.get('2014-02-13'), price=8.4)
        self.assertAlmostEqual(8.4, self.goog.price, delta=0.0001)

    def test_increasing_trend_is_true_if_price_increases_for_3_updates(self):
        self.given_a_series_of_prices([8, 10, 12])
        self.assertTrue(self.goog.is_increasing_trend())

    def test_increasing_trend_is_false_if_price_decreases(self):
        self.given_a_series_of_prices([8, 12, 10])
        self.assertFalse(self.goog.is_increasing_trend())

    def test_increasing_trend_is_false_if_price_is_equal(self):
        self.given_a_series_of_prices([8, 10, 10])
        self.assertFalse(self.goog.is_increasing_trend())

