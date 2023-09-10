import threading


class _thread():
    def __init__(self, stocks) -> None:
        self.stocks = stocks

    def Lookup(self, stock_name):
        if stock_name in self.stocks:
            if self.stocks[stock_name]['volume'] > 10:  # 10 is the limit
                return 0  # Name is found, but trading is suspended due to excessive meme stock trading by the Gauls
            return self.stocks[stock_name]['price']
        else:
            return -1  # Name is not found

    def run(self, queue):
        while True:
            if len(queue) > 0:
                request = queue.pop(0)
                c = request[1]
                stockName = request[0]
                stockPrice = self.Lookup(stockName)
                c.send(str(stockPrice).encode('utf-8'))


class ThreadPool:
    def __init__(self, num, stocks):
        self.thread = _thread(stocks)
        self.request_queue = []
        for i in range(num):
            temp = threading.Thread(target=self.thread.run, args=(self.request_queue,))
            temp.start()

    def add(self, name, c):
        self.request_queue.append([name, c])
