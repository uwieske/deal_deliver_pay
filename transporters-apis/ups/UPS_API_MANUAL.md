# UPS API Manual

## Start the UPS API

It assumed that you have Docker Desktop installed. If not please install Docker Desktop before running the UPS API.

To run the UPS API in Docker container, you need to build the the docker image first.

Cd to the ups directory:
````
docker build . -t upsapi
````

and run the following command to start the UPS API:

````
docker run -d -p 5000:5000 upsapi
````

or if you want to run in interactive mode:
````
docker run -it -p 5000:5000 upsapi
````
The UPS API will listen to port 5000 for incoming HTTP requests.