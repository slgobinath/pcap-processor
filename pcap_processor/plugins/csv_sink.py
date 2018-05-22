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

import csv

from pcap_processor.sink import sink, Sink


@sink(name="csv", enabled=False)
class CsvSink(Sink):

    def __init__(self):
        self.attributes = ['highest_layer', 'transport_layer', 'src_ip', 'dst_ip', 'src_port', 'dst_port',
                           'ip_flag', 'packet_length', 'transport_flag', 'time', 'timestamp', 'geo_country', 'data']
        self.path = "packets.csv"

    def init(self):
        columns = ",".join(self.attributes)
        columns += "\r\n"
        with open(self.path, 'w') as fp:
            fp.write(columns)

    def write(self, packet: dict):
        with open(self.path, 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            row = [packet[attr] for attr in self.attributes]
            writer.writerow(row)

    def close(self):
        pass
