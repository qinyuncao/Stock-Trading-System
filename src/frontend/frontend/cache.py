from threading import Lock

lock = Lock()

# chatgpt基础
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

    def set(self, key, value):
        while lock:
            self.cache[key] = value

    def delete(self, key):
        while lock:
            if key in self.cache:
                del self.cache[key]

cache_instance = SimpleCache()