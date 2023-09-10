response = """\
HTTP/1.1 {status_code} {status_msg}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

frontEndService_addr = '0.0.0.0'
catalogService_addr = '0.0.0.0'
orderService_addr = '0.0.0.0'
catalogSender_addr = '127.0.0.1'
orderSender_addr = '127.0.0.1'
order_port_list = [6000, 6001, 6002]