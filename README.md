# Stock Trading System

This project was done in CompSci 677 from UMass Amherst, by Qinyun Cao and Junzhu Li (in no particular order).

It provides an in-depth exploration of the principles of distributed systems and advanced concepts in operating systems, covering client-server programming, the gRPC framework, multiple microservices architecture, distributed scheduling, HTTP frameworks, REST APIs, virtualization, cloud computing, Docker, caching, AWS Cloud, etc.


## Lab 1
This lab consists of three parts aimed at teaching students various aspects of designing distributed client-server applications. 
### Part 1
It creates a thread pool and implements a socket-based client-server application for online stock trading. The server responds to lookup queries for stock prices, demonstrating the inner workings of thread pools. 

### Part 2 
It shifts to gRPC and built-in thread pools, with the server offering three gRPC calls for stock lookup, trading, and price updates. It also handles synchronization and has error handling, reflecting modern distributed application design. 
### Part 3
Evaluation of our implementations' performance is implemented, including conducting load tests, varying the number of clients, and measuring response times for lookup and trade requests, aiming to gain insights into the efficiency of different design choices and the impact of load on response times.

## Lab 2
It focuses on designing and implementing a microservices-based stock trading application with a two-tier architecture. The goals of the lab include learning distributed system design, containerizing it with Docker, virtualization, web application interfaces, and modern technology implementation. It emphasizes the development of a front-end service, a catalog service, and an order service to handle stock trading operations.

### Part 1
It implements details of the microservices, including the front-end service responsible for stock lookup and trade requests, the catalog service for managing stock data, and the order service for processing trading orders. It emphasizes the importance of concurrency handling and describes the communication mechanisms between these services.

### Part 2 
It discusses containerizing the application using Docker and Docker Compose, ensuring that the microservices can be easily deployed and scaled in a distributed environment. It highlights the need to persist data and handle network configurations when using containers.

### Part 3 
It addresses testing and performance evaluation. It suggests creating test cases to validate the functionality and error handling of the application. Additionally, it proposes performance testing with varying client loads and requests, focusing on latency measurements and discussing the impact of Docker containers on performance.


## Lab 3
It focuses on enhancing the stock trading application by implementing caching, replication, and fault tolerance mechanisms. The application comprises three microservices: front-end, catalog, and order services. 
### Part 1 
It introduces caching to reduce stock query request latency, with cache consistency ensured through a server-push technique. 
### Part 2 
It discusses replication for the order service, aiming to maintain data consistency and fault tolerance with a leader-follower architecture. 
### Part 3 
It deals with handling crash failures and synchronization of replicas.

In summary, this repository outlines a lab project that aims to improve the stock trading application's performance, reliability, and fault tolerance through the implementation of caching, replication, and fault tolerance mechanisms, with a focus on a leader-follower architecture and AWS deployment for evaluation.
