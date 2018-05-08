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

from pcap_processor.map_manager import Map, mapper


@mapper(name="protocol", enabled=False)
class ProtocolMap(Map):

    def map(self, packet: dict):
        highest_layer = packet["highest_layer"]
        if highest_layer in ["XML", "JSON", "DATA-TEXT-LINES"]:
            packet["highest_layer"] = "TEXT"
        elif highest_layer in ["PNG", "MP4", "MEDIA", "IMAGE-JFIF", "IMAGE-GIF"]:
            packet["highest_layer"] = "BINARY"
        elif highest_layer in ["BJNP", "MDNS"]:
            packet["highest_layer"] = "LAN_DISCOVERY"
        elif highest_layer in ["DCERPC", "LSARPC", "RPC_NETLOGON"]:
            packet["highest_layer"] = "RPC"
        elif highest_layer in ["IGMP", "ICMPV6"]:
            packet["highest_layer"] = "ICMP"
        elif highest_layer == "SMB2":
            packet["highest_layer"] = "SMB"
        elif highest_layer == "URLENCODED-FORM":
            packet["highest_layer"] = "HTTP"
        return packet
