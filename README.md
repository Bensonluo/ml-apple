# ml-apple
this is a simple image classifiation server


```
docker pull mongo
```
```
docker run -p 27017:27017 -v D:/develop/data/db --name docker_mongodb -d mongo
```


```
curl -k -X POST -F "image=@Cat_07464.jpg" "http://localhost:5000/predict"
```

bind  the server container port to the local port
```
docker run -d -p 8080:80 ml-apple
```