import json
from threading import Lock

lock = Lock()


class SimpleCache:
    def __init__(self, cache_limit):
        self.cache = []
        self.cache_limit = cache_limit

    def inCache(self, stockName):
        with lock:
            for item in self.cache:
                if item['stockName'] == stockName:
                    return True
            return False

    def add(self, stock):
        with lock:
            if len(self.cache) >= self.cache_limit:
                self.cache.pop(0)
            self.cache.append(json.loads(stock))

    def getStock(self, stockName):
        with lock:
            for item in self.cache:
                if item['stockName'] == stockName:
                    return json.dumps(item)
            return None
        
    def updateStock(self, stockName, amount, type):
        # Process trading update in cache
        with lock:
            for item in self.cache:
                if item['stockName'] == stockName:
                    if type is True:
                        item['quantity'] += amount
                    else:
                        item['quantity'] -= amount
