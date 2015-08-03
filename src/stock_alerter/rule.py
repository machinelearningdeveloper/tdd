class PriceRule:
    """PriceRule is a rule that triggers when a stock price
    satisfies a condition (usually greater, equal or lesser
    than a given value).
    """

    def __init__(self, symbol, condition):
        self.symbol = symbol
        self.condition = condition

    def matches(self, exchange):
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return self.condition(stock) if stock.price else False

    def depends_on(self):
        return {self.symbol}

class AndRule:
    """AndRule is a rule that triggers when all
    component rules trigger.
    """

    def __init__(self, *rules):
        self.rules = rules

    def matches(self, exchange):
        for rule in self.rules:
            if not rule.matches(exchange):
                return False
        else:
            return True