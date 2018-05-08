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

import inspect
from abc import ABC

from pcap_processor.plugin import Plugin


class Map(ABC):

    def map(self, packet: dict):
        return packet


class MapperManager(object):
    mappers = {}

    @classmethod
    def register(cls, mapper_clazz: Map, name, enabled):
        cls.mappers[name] = Plugin(mapper_clazz, enabled)

    @classmethod
    def enable(cls, names):
        """
        Enable only the given list of names and disable the rest.
        :param names: list of reporter names
        :return: None
        """
        for name, plugin in cls.mappers.items():
            plugin.enabled = name in names

    @classmethod
    def map(cls, packet: dict):
        for plugin in cls.mappers.values():
            if plugin.enabled:
                packet = plugin.instance.map(packet)
        return packet


def mapper(name, enabled=False):
    def _mapper(clazz):
        if inspect.isclass(clazz):
            if not hasattr(clazz, "map") or len(inspect.signature(getattr(clazz, "map")).parameters.items()) != 2:
                raise RuntimeError("Map must have a function 'map(self, packet: dict)")
        else:
            raise RuntimeError("Map must be a class")

        # Register the mapper
        MapperManager.register(clazz, name, enabled)
        return clazz

    return _mapper
