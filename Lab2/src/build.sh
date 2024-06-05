docker build . -f catalog_Dockerfile -t catalog
docker build . -f frontend_Dockerfile -t frontend
docker build . -f order_Dockerfile -t order
docker run --name catalog  -d -p 7090:7090 catalog
docker run --name order  -d -p 9090:9090 order
docker run --name frontend  -d -p 6060:6060 frontend