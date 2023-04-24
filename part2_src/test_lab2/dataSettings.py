response = """\
HTTP/1.1 {status_code} {status_msg}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

frontEndService_addr = ('127.0.0.1', 8080)
catalogService_addr = ('127.0.0.1', 7090)
orderService_addr = ('127.0.0.1', 9090)
