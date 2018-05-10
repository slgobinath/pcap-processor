#!/usr/bin/env python3
# pcap-reader - Read and process pcap files using this nifty tool.

# Copyright (C) 2018  Gobinath

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

import grpc

from pcap_processor.grpc import WisdomGrpcService_pb2
from pcap_processor.grpc import WisdomGrpcService_pb2_grpc
from pcap_processor.sink import sink, Sink


@sink(name="grpc", enabled=False)
class GrpcSink(Sink):

    def __init__(self):
        self.endpoint = "localhost:8081"
        self.channel = None
        self.stub = None

    def init(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = WisdomGrpcService_pb2_grpc.WisdomStub(self.channel)

    def write(self, packet: dict):
        self.stub.send(WisdomGrpcService_pb2.Event(data=json.dumps(packet)))

    def close(self):
        self.stub = None
        self.channel = None
