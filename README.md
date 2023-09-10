# Stock Trading System

This project was done in CompSci 677 - UMass Amherst by Qinyun Cao and Junzhu Li (in no particular order).

It provides an in-depth examination of the principles of distributed systems and advanced concepts in operating systems, covering client-server programming, the gRPC framework, multiple microservices architecture, distributed scheduling, HTTP frameworks, REST APIs, virtualization, cloud computing, Docker, caching, AWS Cloud, etc.


## Lab 1
This lab consists of three parts aimed at teaching students various aspects of designing distributed client-server applications. In Part 1, students are tasked with creating a thread pool and implementing a socket-based client-server application for online stock trading. The server responds to lookup queries for stock prices, demonstrating the inner workings of thread pools. Part 2 shifts to gRPC and built-in thread pools, with the server offering three gRPC calls for stock lookup, trading, and price updates. Students are encouraged to handle synchronization and error handling, reflecting modern distributed application design. In Part 3, students evaluate their implementations' performance by conducting load tests, varying the number of clients, and measuring response times for lookup and trade requests, aiming to gain insights into the efficiency of different design choices and the impact of load on response times.
## Lab 2
This paper outlines Lab 2, titled "Asterix and the Microservice Stock Bazaar," which focuses on designing and implementing a microservices-based stock trading application with a two-tier architecture. The goals of the lab include learning distributed system design, virtualization, web application interfaces, and modern technology implementation. It emphasizes the development of a front-end service, a catalog service, and an order service to handle stock trading operations.

In Part 1, the paper discusses the implementation details of the microservices, including the front-end service responsible for stock lookup and trade requests, the catalog service for managing stock data, and the order service for processing trading orders. It emphasizes the importance of concurrency handling and describes the communication mechanisms between these services.

Part 2 discusses containerizing the application using Docker and Docker Compose, ensuring that the microservices can be easily deployed and scaled in a distributed environment. It highlights the need to persist data and handle network configurations when using containers.

Finally, Part 3 addresses testing and performance evaluation. It suggests creating test cases to validate the functionality and error handling of the application. Additionally, it proposes performance testing with varying client loads and requests, focusing on latency measurements and discussing the impact of Docker containers on performance.

In summary, Lab 2 involves designing and implementing a microservices-based stock trading application, containerizing it with Docker, and conducting testing and performance evaluation to ensure functionality and efficiency.
## Lab 3
This paper describes a lab project focused on enhancing the stock trading application by implementing caching, replication, and fault tolerance mechanisms. The application comprises three microservices: front-end, catalog, and order services. Part 1 introduces caching to reduce stock query request latency, with cache consistency ensured through a server-push technique. Part 2 discusses replication for the order service, aiming to maintain data consistency and fault tolerance with a leader-follower architecture. Finally, Part 3 deals with handling crash failures and synchronization of replicas, while Part 4 entails testing and evaluation, including deployment on AWS and latency measurement for different request types.

In summary, the paper outlines a lab project that aims to improve the stock trading application's performance, reliability, and fault tolerance through the implementation of caching, replication, and fault tolerance mechanisms, with a focus on a leader-follower architecture and AWS deployment for evaluation.
