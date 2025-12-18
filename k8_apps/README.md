# Apps
These apps can be used on the cluster to benchmark it. 

## Build
Make sure to build for all platforms, maybe using something like `docker buildx`
```
docker buildx build   --platform linux/amd64,linux/arm64   -t ghcr.io/kr-0-n/master_thesis/server:latest   -f server.Dockerfile   --push .
```
```
