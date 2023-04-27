import socket
import json
from threading import Thread
from dataSettings import *
from flask import Flask, request
from cache import *
import os

app = Flask(__name__)
fAddr = frontEndService_addr
oAddr = orderService_addr
cAddr = catalogService_addr
oSAddr = (os.getenv("PG_HostO", "127.0.0.1"), 9090)
cSAddr = (os.getenv("PG_HostC", "127.0.0.1"), 7090)


class frontEnd:
    def __init__(self, *args, **kwargs):
        self.cache = SimpleCache(3)
        pass

    @app.route('/lookup', methods=['GET'])
    def get_request(self):
        stockName = request.args.get('stockName')
        print(stockName)

        if self.cache.inCache(stockName):
            payload = json.dumps(self.cache.getStock(stockName))#改成有data的格式
            return payload
        else:
            s = socket.socket()
            s.connect(cSAddr)
            lookup_msg = 'Lookup {stock_name}'.format(stock_name=stockName)
            s.send(lookup_msg.encode())
            lookup_response = s.recv(1024).decode('utf-8')
            s.close()

            status_code = lookup_response.split('/')[0]
            res_msg = lookup_response.split('/')[1]

            if status_code == "200":
                reply = json.dumps(res_msg)

                replyTemp = reply.json()
                stockInCache = json.dumps(
                    {
                        "stockName": replyTemp['data']['stockName'],
                        "price": replyTemp['data']['price'],
                        "quantity": replyTemp['data']['quantity']
                    }
                )
                self.cache.add(stockInCache)
                return reply
            else:
                reply = json.dumps(res_msg)
                return reply

    @app.route('/order', methods=['POST'])
    def post_request(self):
        data = request.data
        data = eval(str(data, 'utf-8'))
        stockName = data['stockName']
        quantity = data['quantity']
        tradeType = data['type']
        if self.cache.inCache(stockName):
            if tradeType == "buy":
                self.cache.updateStock(stockName, quantity, False)
            else:
                self.cache.updateStock(stockName, quantity, True)

        s = socket.socket()
        s.connect(oSAddr)
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                       stock_name=stockName)
        s.send(order_msg.encode())
        order_response = s.recv(1024).decode('utf-8')
        s.close()

        status_code = order_response.split("/")[0]
        res_msg = order_response.split("/")[1]
        if status_code == "200":
            reply = json.dumps(res_msg)
            return reply
        else:
            reply = json.dumps(res_msg)
            if self.cache.inCache(stockName):
                if tradeType == "buy":
                    self.cache.updateStock(stockName, quantity, True)
                else:
                    self.cache.updateStock(stockName, quantity, False)
            return reply


if __name__ == '__main__':
    front_end = frontEnd()
    port = 6060
    Thread().start()
    app.run(host='0.0.0.0',port=port,debug=True,threaded=True)
