class Stock:
    @property
    def price(self):
        if self.price_history:
            return self.price_history[-1]
        return None

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError('negative price')
        self.price_history.append(price)

    def is_increasing_trend(self):
        return self.price_history[-3] < self.price_history[-2] < self.price_history[-1]