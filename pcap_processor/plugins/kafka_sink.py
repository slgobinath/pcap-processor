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

from kafka import KafkaProducer

from pcap_processor.sink import sink, Sink


@sink(name="kafka", enabled=False)
class KafkaSink(Sink):

    def __init__(self):
        self.bootstrap = "localhost:9092"
        self.topic = "PacketStream"
        self.key = "pcap-processor"
        self.producer = None

    def init(self):
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap, key_serializer=str.encode,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def write(self, packet: dict):
        self.producer.send(self.topic, key=self.key, value=packet)

    def close(self):
        self.producer.close()
