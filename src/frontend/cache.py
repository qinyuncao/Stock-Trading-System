from threading import Lock

lock = Lock()

class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        while lock:
            return self.cache.get(key, None)
    
    def inCache(self, key):
        while lock:
            if self.cache.get(key):
                return True
            else:
                return False

    def add(self, name, price, quantity):
        while lock:
            self.cache.update({name: {"price": price, "quantity": quantity}})

    def delete(self, key):
        while lock:
            if key in self.cache:
                del self.cache[key]

