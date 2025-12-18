# API Server
Refer to the `proto/message.proto` file to learn about the structure of the messages/services.

## Setup
Install `rust` with `cargo` and `protobuf`

## Get started
Build the project with `cargo build`

## Test
You can use `grpcurl` to test the service.\
**Insert**\
`grpcurl -plaintext -d '{"from": "NodeB", "to": "NodeA", "latency": 20, "throughput": 100}' -proto message.proto
  127.0.0.1:50051 links.LinkService/SendData`

**Get**\
`grpcurl -plaintext -d '{}' -proto message.proto
  127.0.0.1:50051 links.LinkService/GetAllLinks`
