# Instructions for building, tagging, pushing, and running the simex docker container
## Building
```
./build_image.sh
```

## Tag
```
docker tag simex cfgrote/simex
```

## Push
```
docker push cfgrote/simex
```

## Run container and start jupyter to be accessed from host or remote client on port `HOSTPORT`.
```
docker run -p HOSTPORT:24306 cfgrote/simex 
```


