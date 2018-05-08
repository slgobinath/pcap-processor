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


class Sink(ABC):

    def write(self, packet: dict):
        pass

    def init(self):
        pass

    def close(self):
        pass


class SinkManager(object):
    sinks = {}

    @classmethod
    def register(cls, mapper_clazz: Sink, name, enabled):
        cls.sinks[name] = Plugin(mapper_clazz, enabled)

    @classmethod
    def enable(cls, names):
        """
        Enable only the given list of names and disable the rest.
        :param names: list of reporter names
        :return: None
        """
        for name, plugin in cls.sinks.items():
            plugin.enabled = name in names

    @classmethod
    def init(cls):
        for plugin in cls.sinks.values():
            if plugin.enabled:
                plugin.instance.init()

    @classmethod
    def write(cls, packet: dict):
        for plugin in cls.sinks.values():
            if plugin.enabled:
                plugin.instance.write(packet)

    @classmethod
    def close(cls):
        for plugin in cls.sinks.values():
            if plugin.enabled:
                plugin.instance.close()


def sink(name, enabled=False):
    def _sink(clazz):
        if inspect.isclass(clazz):
            if not hasattr(clazz, "write") or len(inspect.signature(getattr(clazz, "write")).parameters.items()) != 2:
                raise RuntimeError("Sink must have a function 'write(self, packet: dict)")
            if not hasattr(clazz, "init") or len(inspect.signature(getattr(clazz, "init")).parameters.items()) != 1:
                raise RuntimeError("Sink must have a function 'init(self)")
            if not hasattr(clazz, "close") or len(inspect.signature(getattr(clazz, "close")).parameters.items()) != 1:
                raise RuntimeError("Sink must have a function 'close(self)")
        else:
            raise RuntimeError("Sink must be a class")

        # Register the sink
        SinkManager.register(clazz, name, enabled)
        return clazz

    return _sink
