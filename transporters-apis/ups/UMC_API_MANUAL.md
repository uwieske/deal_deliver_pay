# UMC API Manual
Our fictive transporter is the result of the inspiration of UPS. 

## Start the UMC API

It assumed that you have Docker Desktop installed. If not please install Docker Desktop before running the UMC API.

To run the UMC API in Docker container, you need to build the the docker image first.

Cd to the ups directory:
````
docker build . -t upsapi
````

and run the following command to start the UMC API:

````
docker run -d -p 5000:5000 upsapi
````

or if you want to run in interactive mode:
````
docker run -it -p 5000:5000 upsapi
````
The UMC API will listen to port 5000 for incoming HTTP requests.