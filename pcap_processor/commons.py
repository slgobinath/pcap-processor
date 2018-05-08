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
import logging.config
import os

import yaml

from pcap_processor import BIN_DIRECTORY

DEFAULT_LOG_CONFIG = os.path.join(BIN_DIRECTORY, 'resources/logging.yaml')


def colorPrint(message, color):
    print("\033[%sm%s\033[0m" % (color, message))


def info(message):
    colorPrint(message, "34")


def warn(message):
    colorPrint(message, "35")


def error(message):
    colorPrint(message, "31")


def setup_logging(default_path=DEFAULT_LOG_CONFIG, default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
