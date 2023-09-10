## Introduction
In this lab, we are required to design distributed server applications using a multi-tier architecture and microservices. The front-end is implemented as a single microservice, while the back-end is implemented as two separate services: a stock catalog service and an stock order service.

## Front end server
It should be able to receive requests from Client, forward the requests to the other two services to handle the request, and send the response back to Client.

### Connect with Client
It receives HTTP GET and HTTP POST requests from the Client, which are `GET /stocks/<stock_name>` and `POST /orders`.

### Connect with Catalog Server after a receiving HTTP GET request
In function `get_request`:
1. Create a socket connecting to Catalog Server.
2. Send the `Lookup` request to Catalog Server.
3. Receive the response from Caralog Server.
4. Send the HTTP response to Client.
* If the lookup request is successful, the response contains `name`, `price` and `quantity` of the stock.
* If it's invalid, the response should contain an `error code` and `error message`.

### Connect with Order Server after a receiving HTTP POST request
In function `post_request`:
1. Create a socket connecting to Order Server.
2. Send the `order` request to Order Server.
3. Receive the response from Order Server.
4. Send the response to Client.
* If the trade is successful, the response contains `transaction_number` of the stock.
* If it's invalid, the response should contain `error code` and `error message`.

## Catalog server
The stock catalog service should maintain a list of all stocks traded in the stock market, the trading volume of each stock and the number of stocks available for sale. 
It should be able to receive requests from Front End Server and Order Server, process their requests and then forward the responses back to these two servers.
> Everytime when we access the database, we should use read-write locks for higher and safer performance.

### Connect with Front End Server
In function `Lookup`:
1. Receive `Lookup` request from Front End Server.
2. Extract the name of the stock in the request.
3. Access the database for the information of the stock.
4. Send the response to Front End Server.
* If the stock exists in the database, the response contains `name`, `price` and `quantity` of the stock.
* If the stock is invalid, the response contains `error code` and `error message`.

### Connect with Order Server
In function `Update`:
1. Receive `order` request from Order Server.
2. Access the database.
3. If the trade type is `sell`, increment the number of the stock in database, and send the status code back to Order Server.
4. If the trade type `buy`, we need to check if the remaining number of the stock is larger than the trading volume in the request. 
- If so, decrement the the number of the stock in database, and send the status code back to Order Server.
- If not, send an `error code` back to Order Server.

## Order server
The Order server should be able to receive requests from Front End Server, forward the requests to Catalog Server, and then send the response from Catalog to Front End.
In function `trade`:
1. Receive `order` request from Front End Server.
2. Connect with Catalog Server using socket.
3. Send the request to Catalog Server.
4. Receive the `status code` from Catalog Server.
5. Send the response to Front End Server.
* If the `status code` is 400, the response should contains `error code` and `error message`.
* If the `status code` is 200, the response should contains `transaction number`.


## Client
The client should be able to send get/post request from client to Front End server.
It used requests to send in HTTP format.
It will Lookup a random stock first.
Then, it has probability p to send another order request in random amount 1-1000, and it will be 50% to buy and 50 % to sell.
It will print what we got from the front end server in terminal.


## Work Distribution
### Part 1
Three services are mainly implemented by Junzhu Li.
HTTP connections and Client are mainly designed by Qinyun Cao.
### Part 2
Docker is mainly written by Qinyun Cao.



## References
[1] https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

[2] https://www.datacamp.com/tutorial/making-http-requests-in-python

[3] https://www.w3schools.com/python/python_json.asp

[4] https://docs.python.org/3/library/http.server.html

[5] https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify

[6] https://stackoverflow.com/questions/43117429/how-to-pass-container-ip-as-env-to-other-container-in-docker-compose-file