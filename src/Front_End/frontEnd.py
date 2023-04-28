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
# oSAddr = (os.getenv("PG_HostO", "127.0.0.1"), 6001)
cSAddr = (os.getenv("PG_HostC", "127.0.0.1"), 7090)
cache = SimpleCache(3)


@app.route('/lookUp', methods=['GET'])
def get_request():
    # handle GET request from client
    stockName = request.args.get('stockName')

    # check cache first
    if cache.inCache(stockName):
        payload = json.dumps(cache.getStock(stockName))
        return payload
    else:
        # connect with catalog service
        s = socket.socket()
        s.connect(cSAddr)
        # forward the request to catalog service
        lookup_msg = 'Lookup {stock_name}'.format(stock_name=stockName)
        s.send(lookup_msg.encode())
        lookup_response = s.recv(1024).decode('utf-8')
        s.close()

        status_code = lookup_response.split('/')[0]
        res_msg = lookup_response.split('/')[1]

        if status_code == "200":
            # handle successful lookup from catalog
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


# --------------原代码-------------- #
# @app.route('/order', methods=['POST'])
# def post_request():
#     data = request.get_json()
#     data = json.loads(data)
#
#     stockName = data['stockName']
#     quantity = data['quantity']
#     tradeType = data['type']
#     if cache.inCache(stockName):
#         if tradeType == "buy":
#             cache.updateStock(stockName, quantity, False)
#         else:
#             cache.updateStock(stockName, quantity, True)
#
#     s = socket.socket()
#     s.connect(oSAddr)
#     order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
#                                                                    stock_name=stockName)
#     s.send(order_msg.encode())
#     order_response = s.recv(1024).decode('utf-8')
#     s.close()
#
#     status_code = order_response.split("/")[0]
#     res_msg = order_response.split("/")[1]
#     if status_code == "200":
#         reply = json.dumps(res_msg)
#         return reply
#     else:
#         reply = json.dumps(res_msg)
#         if cache.inCache(stockName):
#             if tradeType == "buy":
#                 cache.updateStock(stockName, quantity, True)
#             else:
#                 cache.updateStock(stockName, quantity, False)
#         return reply


@app.route('/order', methods=['POST'])
def post_request():
    # handle POST request from client
    data = request.get_json()
    data = json.loads(data)
    stockName = data['stockName']
    quantity = data['quantity']
    tradeType = data['type']

    # if stock is in cache, update in cache
    if cache.inCache(stockName):
        if tradeType == "buy":
            cache.updateStock(stockName, quantity, False)
        else:
            cache.updateStock(stockName, quantity, True)

    # If stock is not in cache, frontend needs to forward request to order service
    order_ports = [6000, 6001, 6002]
    order_Addr = []
    for port in order_ports:
        order_Addr.append((os.getenv("PG_HostO", "127.0.0.1"), port))

    # Send health check msg to order services
    health_check_msg = 'health check'
    alive_port = []
    for i in len(order_Addr):
        s = socket.socket()
        s.connect(order_Addr[i])
        s.send(health_check_msg.encode())
        health_response = s.recv(1024).decode('utf-8')
        # health_reponse = 'alive {order_port}'
        status = health_response.split("/")[0]
        port = health_response.split("/")[1]
        alive_port.append(port)
        s.close()

    # Elect leader with the highest port number
    #----------需要加“没有一个alive的port”的处理吗？----------#
    alive_port.sort(reverse=True)
    leader_port = alive_port[0]
    # Forward order request to leader
    order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                   stock_name=stockName)
    leaderAddr = (os.getenv("PG_HostO", "127.0.0.1"), leader_port)
    s = socket.socket()
    s.connect(leaderAddr)
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
