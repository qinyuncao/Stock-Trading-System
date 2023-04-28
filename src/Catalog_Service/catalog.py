import socket
import json
from threading import Lock, Thread
from dataSettings import *

cAddr = catalogService_addr
lock = Lock()


class CatalogService:
    def __init__(self, *args, **kwargs):
        self.memory = json.load(open('database.json'))

    # Based on the request send by front end, check if the database have the stock. If yes, return it. If not,
    # return 404.
    def Lookup(self, c, request):
        # request message from front end is 'Lookup {stock_name}'
        stock_name = request.split()[1]
        lock.acquire()
        if stock_name in self.memory:
            info = self.memory[stock_name]
        else:
            info = "404"
        lock.release()
        print(info)
        if info != "404":
            price, quantity = info['price'], info['quantity']
            payload = json.dumps(
                {
                    "data": {
                        'stockName': stock_name,
                        'price': price,
                        'quantity': quantity
                    }
                }
            )
            reply_msg = '{code}/{payload}'.format(code=200, payload=payload)
            c.send(reply_msg.encode('utf-8'))
        else:
            payload = json.dumps(
                {
                    "error": {
                        "code": 404,
                        "message": "stock not found"
                    }
                }
            )
            reply_msg = '{code}/{payload}'.format(code=404, payload=payload)
            c.send(reply_msg.encode('utf-8'))
        c.close()

    # Received request from Order_Service
    # i) check if the trade can be made
    # ii) update the database 
    def Update(self, c, request):
        tradeType = request.split(' ')[1]
        quantity = int(request.split(' ')[2])
        stockName = request.split(' ')[3]

        if tradeType == 'sell':
            lock.acquire()
            with open('database.json', 'r+') as f:
                data = json.load(f)
                self.memory[stockName]['quantity'] += quantity
                data[stockName]['quantity'] = self.memory[stockName]['quantity']
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            lock.release()
            reply = "200"
            c.send(reply.encode())

        elif tradeType == 'buy':
            # Check if the trade is valid
            if self.memory[stockName]['quantity'] < quantity:
                lock.acquire()
                reply = "400"
                c.send(reply.encode())
                lock.release()

            elif self.memory[stockName]['quantity'] >= quantity:
                lock.acquire()
                with open('database.json', 'r+') as f:
                    data = json.load(f)
                    self.memory[stockName]['quantity'] -= quantity
                    data[stockName]['quantity'] = self.memory[stockName]['quantity']
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                reply = "200"
                c.send(reply.encode())
                lock.release()

    def catalogHandler(self, c):
        request = c.recv(1024).decode('utf-8')
        print("received request")
        action = request.splitlines()[0].split(' ')[0]
        # Handle request from Front End
        if action == 'Lookup':
            self.Lookup(c, request)
        # Handle request from Order_Service
        else:
            self.Update(c, request)
        return


if __name__ == '__main__':
    catalogService = CatalogService()
    port = 7090
    host = cAddr
    s = socket.socket()
    s.bind((cAddr, port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        Thread(target=catalogService.catalogHandler, args=(c,)).start()
