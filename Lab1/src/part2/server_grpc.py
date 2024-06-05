import grpc
from concurrent import futures
import stockSystem_pb2 as pb2
import stockSystem_pb2_grpc as pb2_grpc
from dataset import *
from threading import Lock


lock = Lock()

class stockSystemServer(pb2_grpc.stockSystemServicer):


    def __init__(self, *args, **kwargs):
        pass

    def Lookup(self, request, context):
        # obtain request
        name = request.stock_name

        lock.acquire()
        stock = stock_list.get(name)
        lock.release()
        if stock:  # dataset has the specific stock
            lock.acquire()
            price = stock_list.get(name)['price']
            volume = stock_list.get(name)['volume']
            lock.release()
            return pb2.PriceVolume(stock_price=price, stock_volume=volume)
        else:
            return pb2.PriceVolume(stock_price=-1, stock_volume=-1)  # an invalid stock name is specified
        
    def Trade(self, request, context):
        # obtain request
        name = request.stock_name
        N = request.num
        type = request.trade_type
        indicator = 0  # stock trading is suspended

        lock.acquire()
        stock = stock_list.get(name)
        lock.release()

        if not stock:
            indicator = -1  # an invalid stock name is specified
        else:
            lock.acquire()
            volume = stock_list.get(name)['volume']
            max = stock_list.get(name)['max_volume']
            lock.release()
            if type == "buy":
                volume += N    
                if volume <= max:
                    indicator = 1
                    lock.acquire()
                    stock_list.get(name)['volume'] = volume
                    lock.release()
            elif type == "sell":
                volume -= N
                if volume >= 0:
                    indicator = 1
                    lock.acquire()
                    stock_list.get(name)['volume'] = volume
                    lock.release()
        return pb2.statusIndicator(status_indicator = indicator)
    
    def Update(self, request, context):
        name = request.stock_name
        price = request.stock_price
        indicator = 0
        
        lock.acquire()
        stock = stock_list.get(name)
        lock.release()

        if not stock:
            indicator = -1  # an invalid stock name is specified
        elif price < 0:
            indicator = -2  # an invalid price (e.g, negative value) is specified
        else:
            lock.acquire()
            stock_list.get(name)['price'] = price
            lock.release()
            indicator = 1  # update is successful
        return pb2.statusIndicator(status_indicator = indicator)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    pb2_grpc.add_stockSystemServicer_to_server(stockSystemServer(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

