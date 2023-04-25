from cache import *
import socket
import json
from threading import Thread
from dataSettings import *
import os
from flask import Flask
app = Flask(__name__)

fAddr = frontEndService_addr
oAddr = orderService_addr
cAddr = catalogService_addr
oSAddr = (os.getenv("PG_HostO","127.0.0.1"), 9090)
cSAddr = (os.getenv("PG_HostC","127.0.0.1"), 7090)



class frontEnd:
    def __init__(self, *args, **kwargs):
        self.cache_instance = SimpleCache()

    # ----------------------以下comment是chatgpt给出来的---------------------
    # def invalidate_cache(request, stock_id):
    #     self.cache_instance.delete(stock_id)
    #     return JsonResponse({'status': 'success'}, status=200)

    # def query_stock(request, stock_id):
    #     if stock_id in cache:
    #         return JsonResponse(cache[stock_id])

    #     response = requests.get(f'{CATALOG_SERVICE_URL}/stocks/{stock_id}/')
    #     if response.status_code == 200:
    #         stock_data = response.json()
    #         cache[stock_id] = stock_data
    #         return JsonResponse(stock_data)
    #     return JsonResponse({'error': 'Stock not found'}, status=404)
    # ----------------------------结束------------------------------------
    


    # Handle GET request from client and forward it to Catalog_Service
    @app.route('/')
    def get_request(self, c, request):
        msg = request.splitlines()[0].split(' ')[1]
        stock = msg.split('/')[2] #需要对一下看看传回来的是不是这里stock name

        # first check the in-memory cache
        if self.cache_instance.inCache(stock):
            # 需要检查下数据格式
            payload = json.dumps(
                {
                    "data": {
                        'stockName': stock,
                        'price': self.cache_instance.get(stock)['price'],
                        'quantity': self.cache_instance.get(stock)['quantity']
                    }
                }
            )
            c.send(
                response.format(status_code=200, status_msg='OK', content_length=len(payload), payload=payload).encode(
                    "utf-8"))
            
        else: 
            # If not in cache, forward the request to catalog
            s = socket.socket()
            s.connect(cSAddr)
            lookup_msg = 'Lookup {stock_name}'.format(stock_name=stock)
            s.send(lookup_msg.encode())
            lookup_response = s.recv(1024).decode('utf-8')
            s.close()

            status_code = lookup_response.split('/')[0]
            res_msg = lookup_response.split('/')[1]

            if status_code == "200":
                reply = json.dumps(res_msg)
                c.send(
                    response.format(status_code=200, status_msg='OK', content_length=len(reply), payload=reply).encode(
                        "utf-8"))
            else:
                reply = json.dumps(res_msg)
                c.send(
                    response.format(status_code=404, status_msg='Error', content_length=len(reply), payload=reply).encode(
                        "utf-8"))
            
            # Update cache
            if status_code == "200":
                # 需要检查下数据格式
                name = res_msg['data']['stockName']
                quantity = res_msg['data']['quantity']
                price = res_msg['data']['price']
                self.cache_instanceadd(name, price, quantity)
            else:
                # 需要加错误处理？
                pass
                
        c.close()


if __name__ == '__main__':
    front_end = frontEnd()
    # app.run()