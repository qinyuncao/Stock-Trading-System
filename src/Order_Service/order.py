import socket
import json
from threading import Lock, Thread

from dataSettings import *
import os

cAddr = catalogService_addr
oAddr = orderService_addr
cSAddr = (os.getenv("PG_HostC", "127.0.0.1"), 7090)
lock = Lock()
# count1 = -1
# count2 = -1
# count3 = -1
ports = [6000, 6001, 6002]
counts = [0, 0, 0]


def trade(c, msg, leader_port):
    # Process POST from front end （'POST {trade} {num} {name}'）
    # Only leader will receive trade request from front end
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

        i = ports.index(leader_port)
        counts[i] = counts[i] + 1
        cur_counter = counts[i]

        order_history = str(cur_counter) + ' stockName:' + stockName + ",tradeType:" + tradeType + ",quantity:" + str(
            quantity) + '\n'
        file = "order" + str(leader_port) + ".txt"
        with open(file, 'a') as file:
            # write to leader's own database file
            file.write(order_history)

        # 通知follower
        notify_msg = 'notify {order_his}'.format(order_his=order_history)
        print(notify_msg)
        for port in ports:
            if port != leader_port:
                # connect with followers
                follower_socket = socket.socket()
                follower_socket.connect(('localhost', port))
                # send 'notify {order_history}' to followers
                follower_socket.send(notify_msg.encode())
                follower_socket.close()


# 可能有order, leader通知(从frontend），leader给follower发消息，healthcheck（从frontend和从order到order),crash掉以后的同步申请
def handle_client(client_socket, port):
    request = client_socket.recv(1024).decode('utf-8')
    action = request.splitlines()[0].split(' ')[0]
    if action == 'order':
        # leader handle order requests from front end
        trade(client_socket, request, port)
    elif action == 'healthCheck':
        # all order services handle 'health check' from frontend
        health_msg = 'alive {self_port}'.format(self_port=port)
        client_socket.send(health_msg.encode())
    elif action == 'leaderID':
        # ------------follower需要干啥？------------ #
        # all order services handle leader election result 'leaderID: {id}' from front end
        pass
    elif action == 'notify':
        # followers receives 'notify {order_history}' from leader
        order_history = request[7:]
        print(order_history)
        file = "order" + str(port) + ".txt"
        with open(file, 'a') as file:
            # write to follower's own database file
            file.write(order_history)
    return


def start_server(port):
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    server_socket.bind(('localhost', port))
    # listen for incoming connections
    server_socket.listen(1)

    # accept incoming connections and handle them in separate threads
    while True:
        client_socket, address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket, port))
        client_thread.start()


if __name__ == '__main__':
    # port = 9090 改frontend

    # start multiple servers in separate threads
    server_threads = []
    for port in ports:
        filename = "order" + str(port) + ".txt"
        i = ports.index(port)
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in reversed(lines):
                    if int(line.split(' ')[0]) > 0:
                        counts[i] = int(line.split(' ')[0])
        else:
            counts[i] = 0

        server_thread = Thread(target=start_server, args=(port,))
        server_thread.start()
        server_threads.append(server_thread)

    # wait for all threads to finish
    for server_thread in server_threads:
        server_thread.join()
