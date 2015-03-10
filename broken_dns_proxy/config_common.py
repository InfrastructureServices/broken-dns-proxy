# -*- coding: utf-8 -*-
#
# Simple DNS Proxy for simulating DNS issues
# Copyright (C) 2014-2015  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:


class ConfigurableClass(object):
    """
    Super class representing any object that can be possibly
    """

    CONFIG_SECTION_NAME = None

    _options_dict = dict()

    @classmethod
    def config_section_name(cls):
        """
        Return the string with name of the configuration section for the class

        :return: str
        """
        return cls.CONFIG_SECTION_NAME

    @classmethod
    def default_configuration_dict(cls):
        """
        Return dictionary with the default configuration for the class

        :return: dictionary {<option>: <value>, ...}
        """
        return dict(cls._options_dict)


class GlobalConfig(ConfigurableClass):

    # Some configuration values are reserved and not set here as
    # these are read from the command line. Reserved:
    # 'Verbose'
    # 'ConfigPath'
    CONFIG_VERBOSE = 'Verbose'
    CONFIG_CONFIG_PATH = 'ConfigPath'

    CONFIG_SECTION_NAME = 'Proxy'

    CONFIG_PORT = 'Port'
    CONFIG_PORT_VALUE = '53'
    CONFIG_ADDRESS = 'Address'
    CONFIG_ADDRESS_VALUE = ''
    CONFIG_UPSTREAM_SERVERS = 'UpstreamServers'
    CONFIG_UPSTREAM_SERVERS_VALUE = '8.8.8.8 8.8.4.4'
    CONFIG_MODIFIERS = 'Modifiers'
    CONFIG_MODIFIERS_VALUE = ''

    _options_dict = {
        CONFIG_PORT: CONFIG_PORT_VALUE,
        CONFIG_ADDRESS: CONFIG_ADDRESS_VALUE,
        CONFIG_UPSTREAM_SERVERS: CONFIG_UPSTREAM_SERVERS_VALUE,
        CONFIG_MODIFIERS: CONFIG_MODIFIERS_VALUE
    }