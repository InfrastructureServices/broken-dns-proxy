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

import six
from six.moves.configparser import ConfigParser

from broken_dns_proxy.logger import logger
from broken_dns_proxy.proxy_server import ProxyServer


class BrokenDnsProxyConfiguration(object):
    """
    Configuration parser for Broken DNS Proxy
    """

    def __init__(self, cli_conf):
        self._config = ConfigParser()
        self._add_commandline_arguments(cli_conf)
        self._read_proxy_default_config()

        if cli_conf.config_path != self._config.read(cli_conf.config_path):
            logger.warning("Configuration file '{0}' could not be read... "
                           "Using ONLY default settings".format(cli_conf.config_path))

        #  TODO: Read modifiers default configuration based the Proxy config

    def _read_proxy_default_config(self):
        """
        Read the default configuration of Proxy Server and add it to Config

        :return: None
        """
        BrokenDnsProxyConfiguration.config_parser_read_dict(self._config, {ProxyServer.config_section_name():
                                                                           ProxyServer.default_configuration_dict()})

    def _add_commandline_arguments(self, cli_conf):
        """
        Construct a dict from CLI arguments and add it to Config

        :param cli_conf: ArgumentParser object initialized by CLI args
        :return: None
        """
        cli_settings = {ProxyServer.config_section_name(): {
            'Verbose': cli_conf.verbose,
            'ConfigPath': cli_conf.config_path
        }}

        BrokenDnsProxyConfiguration.config_parser_read_dict(self._config, cli_settings)

    @staticmethod
    def config_parser_read_dict(config_parser_obj, dictionary):
        """
        Read dictionary into the ConfigParser. Existing values in ConfigParser
        object are not overwritten. (note: read_dict() is not available in Python 2.7)

        :param config_parser_obj: existing ConfigParser object
        :param dictionary: dictionary to read the config from {<section>: {<option>: <value>, ...}}
        :return: None
        """
        # go through all sections
        for section, conf in six.iteritems(dictionary):
            if config_parser_obj.has_section(section) is False:
                config_parser_obj.add_section(section)

            # go through all key: value in the section
            for option, value in six.iteritems(conf):
                if config_parser_obj.has_option(section, option) is False:
                    config_parser_obj.set(section, option, value)