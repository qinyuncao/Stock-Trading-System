## Introduction
In the last lab, we were required to design distributed server applications using a multi-tier architecture and microservices. We need to add caching, replication, and fault tolerance to our application in this lab..The front-end is implemented as a single microservice, while the back-end is implemented as two separate services: a stock catalog service and an stock order service.


## Front end server
It should be able to receive requests from Client, forward the requests to the other two services to handle the request, and send the response back to Client. It should have caching to reduce the latency of the stock query requests.
We implemented our front end server using flask.


### Connect with Client
It receives GET and POST requests from the Client, which are `GET /stocks/<stock_name>` and `POST /orders`.


### Connect with Catalog Server after receiving GET request
In function `get_request`:
Check its cache first to see if the stock is in cache. If so, send a reponse to Client, containing `name`, `price` and `quantity` of the stock.
If the stock is not in cache:
1. Create a socket connecting to Catalog Server.
2. Forward the `Lookup` request to Catalog Server.
3. Receive the response from Caralog Server.
4. Send the HTTP response to Client.
* If the lookup request is successful, the response contains `name`, `price` and `quantity` of the stock.
* If it's invalid, the response should contain an `error code` and `error message`.


### Connect with Order Server after a receiving POST request
In function `post_request`:
Check its cache first to see if the stock is in cache. If so, update on cache.
1. Send health checking message to leader order server to see if it's alive. If so, create a socket connecting to leader Order Server. If not, process leader election to have another leader order server, and then create a socket connecting to the new leader.
2. Forward the `order` request to the leader.
3. Repeat step 1 until it receives the response from leader.
4. Send the response to Client.
* If the trade is successful, the response contains `transaction_number` of the stock.
* If it's invalid, the response should contain `error code` and `error message`. Then we undo the action we did to cache.

If the stock is not in cache:
* Do not do anything to cache.


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
3. If the trade type is `sell`, increment the nxumber of the stock in database, and send the status code back to Order Server.
4. If the trade type `buy`, we need to check if the remaining number of the stock is larger than the trading volume in the request.
- If so, decrement the the number of the stock in database, and send the status code back to Order Server.
- If not, send an `error code` back to Order Server.


## Order server
The Order server should have three replicas with its own database file after it starts.
After receiving health check message from Front End Server, alive replicas send its status and its port to front end for leader election. Leader should be able to receive POST requests from Front End Server, forward the requests to Catalog Server, send the response from Catalog to Front End, and notify followers.
Followers should be able to update its database file every time leader sends its new order info.
In function `synchronization`:
We initially sychronize three database files so that they should be the same to deal with crash. Our approach is that the latest replica has the largest database file. So the only thing we need to do is just to copy its file to another two.


In function `trade`:
1. Leader receives `order` request from Front End Server.
2. Connect with Catalog Server using socket.
3. Send the request to Catalog Server.
4. Receive the `status code` from Catalog Server.
5. Send the response to Front End Server.
* If the `status code` is 400, the response should contains `error code` and `error message`.
* If the `status code` is 200, the response should contains `transaction number`.
6. Modify its database file and update the latest transaction.
7. Notify followers.


## Client
The client should be able to send get/post request from client to Front End server. It used requests to send in HTTP format. It will Lookup a random stock first. Then, it has probability p to send another order request in random amount 1-1000, and it will be 50% to buy and 50 % to sell. It will print what we got from the front end server in terminal.


## Work Distribution
Front end service's flask API, and implementation of how three order replicas communicate with each other were mainly modified by Qinyun Cao.
Caching, synchronization among three order replicas, and how leader notify followers were mainly designed by Junzhu Li.
We worked on how to go through the whole process of health checking and leader election at the same time.




## References
[1] https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


[2] https://www.datacamp.com/tutorial/making-http-requests-in-python


[3] https://www.w3schools.com/python/python_json.asp


[4] https://docs.python.org/3/library/http.server.html


[5] https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify


[6] https://stackoverflow.com/questions/43117429/how-to-pass-container-ip-as-env-to-other-container-in-docker-compose-file


[7] https://flask.palletsprojects.com/en/2.2.x/
