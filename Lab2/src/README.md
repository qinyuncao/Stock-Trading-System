## Authors 
Junzhu Li, junzhuli@umass.edu

Qinyun Cao, qinyuncao@umass.edu


## Number of late days used for this lab
2

## Number of late days used so far including this lab
3

## Install Docker
Please follow the installations for your operating system. However, It's recommended that you use a Linux machine or virtual machine for this tutorial.
### Linux

For Ubuntu please follow [this guide](https://docs.docker.com/engine/install/ubuntu/) to install
docker engine. If you are using other distros please refer to [this
page](https://docs.docker.com/engine/install/) to check if it's officially supported by Docker.

By default docker requires `root` privileges to run on Linux, therefore you will have to prefix all
the docker commands in this tutorial with `sudo` to run as `root`. If you don't want to run docker
commands without `sudo`, you can either [create a group named `docker` and add your user to this
group](https://docs.docker.com/engine/install/linux-postinstall/) (the `docker` group grants
privileges equivalent to the `root` user), or you can run the docker daemon in [rootless
mode](https://docs.docker.com/engine/security/rootless/) (this is more secure but has certain
limitations).

### Windows

Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/).
Depending on your Windows version, you may need to first [enable WSL 2 or
Hyper-V](https://docs.docker.com/desktop/windows/install/#system-requirements) in order to
successfully install Docker Desktop. After installation please check out the [Docker Desktop for
Windows user manual](https://docs.docker.com/desktop/windows/) for Windows specific settings.

### Mac

Download and install [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/). After
installation please check out the [Docker Desktop for Mac user
manual](https://docs.docker.com/desktop/mac/) for Mac specific settings. The Docker Desktop for mac comes with versions for intel based CPUs and apple silicon CPUs as well. 


## How to Run With Docker

**Requires Python 3.6+**

First run Docker:
```
docker-compose up
```

Then start the client in a separate terminal:
```
python3 client.py
```


## How to Run without docker

**Requires Python 3.6+**

Run the services:
```
python3 catalog.py
python3 order.py
python3 frontEnd.py
```

From another terminal, run the client:
```
python3 client.py
```


## References
[1] https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

[2] https://www.datacamp.com/tutorial/making-http-requests-in-python

[3] https://www.w3schools.com/python/python_json.asp

[4] https://docs.python.org/3/library/http.server.html

[5] https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify

[6] https://stackoverflow.com/questions/43117429/how-to-pass-container-ip-as-env-to-other-container-in-docker-compose-file

[7]https://docs.python.org/3/library/unittest.html