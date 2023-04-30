response = """\
HTTP/1.1 {status_code} {status_msg}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

frontEndService_addr = '0.0.0.0'
catalogService_addr = '0.0.0.0'
orderService_addr = '0.0.0.0'
catalogSender_addr = '3.88.183.128'
orderSender_addr = '3.88.183.128'
