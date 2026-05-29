#!/bin/bash
# Tetra Cell 1
grpcurl -plaintext -d '{"from": "minikube", "to": "minikube-m08", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m08", "to": "minikube", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube", "to": "minikube-m07", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m07", "to": "minikube", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube", "to": "minikube-m06", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m06", "to": "minikube", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m07", "to": "minikube-m06", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m06", "to": "minikube-m07", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m08", "to": "minikube-m06", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m06", "to": "minikube-m08", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m08", "to": "minikube-m07", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m07", "to": "minikube-m08", "latency": 5, "throughput": 0.5}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# Tetra Cell 2
grpcurl -plaintext -d '{"from": "minikube-m03", "to": "minikube-m02", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m02", "to": "minikube-m03", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m02", "to": "minikube-m05", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m05", "to": "minikube-m02", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m05", "to": "minikube-m04", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m04", "to": "minikube-m05", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m03", "to": "minikube-m04", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m04", "to": "minikube-m03", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m03", "to": "minikube-m05", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m05", "to": "minikube-m03", "latency": 10, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m04", "to": "minikube-m02", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m02", "to": "minikube-m04", "latency": 20, "throughput": 0.08}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# Stacom
grpcurl -plaintext -d '{"from": "minikube-m08", "to": "minikube-m05", "latency": 250, "throughput": 0.55}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "minikube-m05", "to": "minikube-m08", "latency": 250, "throughput": 0.55}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# High Speed Link
# grpcurl -plaintext -d '{"from": "minikube", "to": "minikube-m02", "latency": 2, "throughput": 100}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
# grpcurl -plaintext -d '{"from": "minikube-m02", "to": "minikube", "latency": 2, "throughput": 100}' -import-path $HOME/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
