#!/usr/bin/env bash
python3 -m grpc_tools.protoc -I proto --python_out=pcap_processor/grpc --grpc_python_out=pcap_processor/grpc proto/WisdomGrpcService.proto