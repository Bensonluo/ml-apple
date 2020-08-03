# ml-apple
*This is a simple image classifiation server*

Sorry for the unshaped solution due to time limitation

### Tech stack
Backend Language: 	   			Python

Api framework:            			 Flask

Wsgi server:       					   Gunicorn + gevent

Database:                     			MongoDB

API Documentation:   			 swagger

Machine learning model:  	  pretrained MobileNet_v2

Container: docker

Not done yet:  Ngnix

Develope OS env: windows, Linux(with docker)

### Get the server to run on your machine
It should be easy to download docker from [Download](https://docs.docker.com/docker-for-windows/install/)

Then you can pull the code down and navigate to the repo and run
```docker build -t name:v1.0 .```
waiting for the image to be built

After  build successfully executed,
```docker run -d -p 8080:80 name```
will run the container and bind the 80 port to the local 8080 port.

you can also just run it with flask server then heading to 
"http://localhost:5000/"


### MongoDB
similarly, pull the mongoDB image by running
```
docker pull mongo
```
then
```
docker run -p 27017:27017 -v D:/develop/data/db --name docker_mongodb -d mongo
```
which will run the db container and set the data repo, as well as binding the port

### Send a Request
Curl command can be used to test the server or Postman if you feel more comfortable with that.
```
curl -k -X POST -F "image=@image_name.jpg" "http://localhost:5000/predict"
```

### Bind the server container with mongoDB
Following command can make server container to connect with the mongoDB container.
```
docker run -itd -P --name docker_ml --link docker_mongodb:conn ml-apple:latest
```
well, add an env in the end if you want to check binding result
```
docker run --rm --name docker_ml --link docker_mongodb:conn ml-apple:latest env
```