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

import argparse
import os

from pcap_processor import plugin_manager, commons
from pcap_processor.reader import PcapReader


def file_type(path):
    """ArgParse callable to validate positional add-on arguments

    Arguments:
        path {string} -- user defined argument

    Raises:
        argparse.ArgumentTypeError -- thrown when user input is not a directory or does not contain addon.xml

    Returns:
        string -- absolute path of the input directory
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(
            "Pcap file or directory %s does not exist" % path)
    return os.path.abspath(path)


def main():
    commons.setup_logging()
    plugin_manager.load_plugins()
    parser = argparse.ArgumentParser(prog="pcap-processor",
                                     description="Read and process pcap files using this nifty tool.")
    plugin_manager.fill_cmd_args(parser)
    parser.add_argument("--version", action="version",
                        version="%(prog)s 0.0.1")
    parser.add_argument("file", type=file_type, nargs="+", help="pcap file to read")

    args = parser.parse_args()

    pcap_file = args.file
    plugin_manager.process_config(args)
    reader = PcapReader(pcap_file)
    reader.read()


if __name__ == '__main__':
    main()
