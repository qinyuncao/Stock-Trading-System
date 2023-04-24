from django.http import JsonResponse
from . import cache
import requests
from threading import Lock

# 这些都要改
CATALOG_SERVICE_URL = 'http://catalog-service-url' 
CATALOG_SERVICE_URL = 'http://client-url' 


def invalidate_cache(request, stock_id):
    cache_instance.delete(stock_id)
    return JsonResponse({'status': 'success'}, status=200)

def query_stock(request, stock_id):
    if stock_id in cache:
        return JsonResponse(cache[stock_id])

    response = requests.get(f'{CATALOG_SERVICE_URL}/stocks/{stock_id}/')
    if response.status_code == 200:
        stock_data = response.json()
        cache[stock_id] = stock_data
        return JsonResponse(stock_data)
    return JsonResponse({'error': 'Stock not found'}, status=404)

