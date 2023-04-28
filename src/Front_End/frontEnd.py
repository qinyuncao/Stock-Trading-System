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
oSAddr = (os.getenv("PG_HostO", "127.0.0.1"), 6001)
cSAddr = (os.getenv("PG_HostC", "127.0.0.1"), 7090)
cache = SimpleCache(3)


@app.route('/lookUp', methods=['GET'])
def get_request():
    stockName = request.args.get('stockName')

    if cache.inCache(stockName):
        payload = json.dumps(cache.getStock(stockName))
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
            replyTemp = json.loads(res_msg)
            stockInCache = json.dumps(
                {
                    "stockName": replyTemp['data']['stockName'],
                    "price": replyTemp['data']['price'],
                    "quantity": replyTemp['data']['quantity']
                }
            )
            cache.add(stockInCache)
            return reply
        else:
            reply = json.dumps(res_msg)
            return reply


@app.route('/order', methods=['POST'])
def post_request():
    data = request.get_json()
    data = json.loads(data)

    stockName = data['stockName']
    quantity = data['quantity']
    tradeType = data['type']
    if cache.inCache(stockName):
        if tradeType == "buy":
            cache.updateStock(stockName, quantity, False)
        else:
            cache.updateStock(stockName, quantity, True)

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
        if cache.inCache(stockName):
            if tradeType == "buy":
                cache.updateStock(stockName, quantity, True)
            else:
                cache.updateStock(stockName, quantity, False)
        return reply


if __name__ == '__main__':
    port = 6060
    Thread().start()
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
