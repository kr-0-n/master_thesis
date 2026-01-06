# Kubernetes deployments
This folder includes all the different possible deployments. You can apply them if you kubectl config is correct. Use `kubectl apply -f deployment.yml`
## API Server
The API server is bundled into a docker container which is available publicly on `ghcr.io`\
It can be simply deployed by executing `kubectl apply -f api_server.yml`
## Test App
There is a test app which can be deployed to test the network. Multiple instances can be deployed. They consist of one server and at least one client. Each client will then use IPERF and hping to connect to the server. A maximum sending rate can be set by using an env variable.
To deploy an app (which will automatically include all components), use the Kubernetes package manager _helm_ `helm install test-app-1 ./test-app -f values-test.yml`. In the `values-test.yml` file, the config values can be set (Note that the latency value is not in use right now and acts as a placeholder. Bandwidth and replica count work however). Multiple of these can be used at the same time (make sure to use different names)
