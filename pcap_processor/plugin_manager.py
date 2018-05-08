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

import importlib
import os
import pkgutil
import sys
from argparse import ArgumentParser

from pcap_processor.map_manager import MapperManager
from pcap_processor.sink import SinkManager


def load_plugins():
    plugins_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins")
    sys.path.append(plugins_dir)
    for importer, package_name, _ in pkgutil.iter_modules([plugins_dir]):
        if "test_" not in package_name:
            importlib.import_module(package_name)


def fill_cmd_args(parser: ArgumentParser):
    # Add --map
    parser.add_argument("--map", action="append", choices=list(MapperManager.mappers.keys()),
                        help="""enable a mapper with the given name.
                        You can use this option multiple times to enable more than one mappers""")
    parser.add_argument("--sink", action="append", choices=list(SinkManager.sinks.keys()),
                        help="""enable a sink with the given name.
                            You can use this option multiple times to enable more than one sinks""")


def process_config(config):
    mappers = config.map
    sinks = config.sink
    if mappers is not None:
        MapperManager.enable(mappers)
    if sinks is not None:
        SinkManager.enable(sinks)
