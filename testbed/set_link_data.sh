#!/bin/bash
# Tetra Cell 1
grpcurl -plaintext -d '{"from": "multinode", "to": "multinode-m08", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m08", "to": "multinode", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode", "to": "multinode-m07", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m07", "to": "multinode", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode", "to": "multinode-m06", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m06", "to": "multinode", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m07", "to": "multinode-m06", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m06", "to": "multinode-m07", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m08", "to": "multinode-m06", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m06", "to": "multinode-m08", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m08", "to": "multinode-m07", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m07", "to": "multinode-m08", "latency": 5, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# Tetra Cell 2
grpcurl -plaintext -d '{"from": "multinode-m03", "to": "multinode-m02", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m02", "to": "multinode-m03", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m02", "to": "multinode-m05", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m05", "to": "multinode-m02", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m05", "to": "multinode-m04", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m04", "to": "multinode-m05", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m03", "to": "multinode-m04", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m04", "to": "multinode-m03", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m03", "to": "multinode-m05", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m05", "to": "multinode-m03", "latency": 20, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m04", "to": "multinode-m02", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m02", "to": "multinode-m04", "latency": 10, "throughput": 0.5}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# Stacom
grpcurl -plaintext -d '{"from": "multinode-m08", "to": "multinode-m02", "latency": 250, "throughput": 0.55}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "multinode-m02", "to": "multinode-m08", "latency": 250, "throughput": 0.55}' -import-path /home/kron/projects/master_thesis/api_server/proto -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
