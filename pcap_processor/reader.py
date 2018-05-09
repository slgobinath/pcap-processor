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

import logging
import os

import pyshark
from pyshark.capture.capture import TSharkCrashException

from pcap_processor import commons
from pcap_processor.map_manager import MapperManager
from pcap_processor.sink import SinkManager

logger = logging.getLogger(__name__)


class PcapReader:
    def __init__(self, path):
        self.path = path
        self.active = False

    def _read_pcap(self, path):
        logger.debug("Reading pcap file: %s", path)
        packets = pyshark.FileCapture(path)
        for pcap in packets:
            has_transport = pcap.transport_layer is not None
            packet_time = float(pcap.sniff_timestamp)
            packet_dict = dict()
            highest_layer = pcap.highest_layer.upper()
            packet_dict["highest_layer"] = highest_layer
            if has_transport:
                packet_dict["transport_layer"] = pcap.transport_layer.upper()
            else:
                packet_dict["transport_layer"] = "None"
                packet_dict["src_port"] = -1
                packet_dict["dst_port"] = -1
                packet_dict["transport_flag"] = -1

            packet_dict["timestamp"] = int(packet_time * 1000)
            packet_dict["time"] = str(pcap.sniff_time)
            packet_dict["packet_length"] = int(pcap.length)

            for layer in pcap.layers:
                layer_name = layer.layer_name.upper()
                if "IP" == layer_name or "IPV6" == layer_name:
                    packet_dict["src_ip"] = str(layer.src)
                    packet_dict["dst_ip"] = str(layer.dst)
                    if hasattr(layer, "flags"):
                        packet_dict["ip_flag"] = int(layer.flags, 16)
                    else:
                        packet_dict["ip_flag"] = -1
                    if hasattr(layer, "geocountry"):
                        packet_dict["geo_country"] = str(layer.geocountry)
                    else:
                        packet_dict["geo_country"] = "Unknown"

                elif has_transport and layer_name == pcap.transport_layer:
                    packet_dict["src_port"] = int(layer.srcport)
                    packet_dict["dst_port"] = int(layer.dstport)
                    if hasattr(layer, "flags"):
                        packet_dict["transport_flag"] = int(layer.flags, 16)
                    else:
                        packet_dict["transport_flag"] = -1

                elif "FTP" == layer_name:
                    packet_dict["data"] = str(layer._all_fields)
                if "src_ip" not in packet_dict:
                    continue

            # Map packet attributes
            packet_dict = MapperManager.map(packet_dict)
            SinkManager.write(packet_dict)

    def _read_path(self, path):
        if os.path.isfile(path):
            try:
                self._read_pcap(path)
            except TSharkCrashException as ex:
                commons.error("Error in parsing %s pcap file" % path)
        elif os.path.isdir(path):
            # Iterate through all csv files in the directory
            files = os.listdir(path)
            for file in files:
                if file.lower().endswith(".pcap"):
                    pcap_file = os.path.join(path, file)
                    try:
                        self._read_pcap(pcap_file)
                    except TSharkCrashException:
                        commons.error("Error in parsing %s pcap file" % pcap_file)
        else:
            commons.error("Path %s is neither a file nor a directory" % self.path)

    def read(self):
        self.active = True
        SinkManager.init()
        if type(self.path) is list:
            for file in self.path:
                self._read_path(file)
        else:
            self._read_path(self.path)
        SinkManager.close()

    def stop(self):
        self.active = False
