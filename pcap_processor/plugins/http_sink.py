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

import http.client
import json

from pcap_processor.sink import sink, Sink


@sink(name="http", enabled=False)
class HttpSink(Sink):

    def __init__(self):
        self.headers = {"Content-type": "application/json"}
        self.endpoint = "/"
        self.connection = None

    def init(self):
        self.connection = http.client.HTTPConnection("localhost", 8080)

    def write(self, packet: dict):
        self.connection.request("POST", self.endpoint, json.dumps(packet), self.headers)
        self.connection.getresponse().close()

    def close(self):
        self.connection.close()
