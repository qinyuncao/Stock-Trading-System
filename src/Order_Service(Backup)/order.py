import socket
import json
from threading import Lock, Thread
from dataSettings import *
import os


cAddr = catalogService_addr
oAddr = orderService_addr
cSAddr = (os.getenv("PG_HostC","127.0.0.1"), 7090)
lock = Lock()


class OrderService:
    def __init__(self):
        self.file = 'order.txt'

    # Process POST from front end （'POST {trade} {num} {name}'）
    def trade(self, c, msg):
        tradeType = msg.split(' ')[1]
        quantity = msg.split(' ')[2]
        stockName = msg.split(' ')[3]
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                       stock_name=stockName)
        s = socket.socket()
        s.connect(cSAddr)
        s.send(order_msg.encode())
        indicator = s.recv(1024).decode('utf-8')
        s.close()
        print(indicator)

        if indicator == '400':
            payload = json.dumps(
                {
                    "error": {
                        "code": 400,
                        "message": "trade is invalid"
                    }
                }
            )
            reply_msg = '{code}/{payload}'.format(code=400, payload=payload)
            c.send(reply_msg.encode())

        elif indicator == '200':
            payload = json.dumps(
                {
                    "data": {
                        "transaction number": quantity,
                    }
                }
            )
            reply_msg = '{code}/{payload}'.format(code=200, payload=payload)
            c.send(reply_msg.encode())
            order_history = 'stockName:' + stockName + ",tradeType:" + tradeType + ",quantity:" + str(quantity) + '\n'
            f = open(self.file, 'a')
            f.write(order_history)

    def orderHandler(self, c):
        request = c.recv(1024).decode('utf-8')
        action = request.splitlines()[0].split(' ')[0]
        if action == 'order':
            self.trade(c, request)
        return


if __name__ == '__main__':
    order_service = OrderService()
    s = socket.socket()
    port = 9090
    s.bind((oAddr,port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        Thread(target=order_service.orderHandler, args=(c,)).start()
