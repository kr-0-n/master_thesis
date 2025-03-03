# Kubernetes deployments
This folder includes all the different possible deployments. You can apply them if you kubectl config is correct. Use `kubectl apply -f deployment.yml`
## API Server
The image for the API server is in UiO Harbor. To pull from there, you need the correct secret in kubernetes. You can load it in with\
 `kubectl create secret generic regcred --from-file=.dockerconfigjson=config.json --type=kubernetes.io/dockerconfigjson`\
Make sure you have the correct secret. You can obtain it with something like `docker login harbor.uio.no`
## Client Deployment
Nothing interesting here
## Server Deployment
Nothing interesting here