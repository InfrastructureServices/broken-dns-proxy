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

import os
import six
from six.moves.configparser import ConfigParser

from broken_dns_proxy.logger import logger
from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.modifiers import get_modifier_by_name
from broken_dns_proxy.config_common import GlobalConfig


class BrokenDnsProxyConfiguration(object):
    """
    Configuration parser for Broken DNS Proxy
    """

    def __init__(self, cli_conf):
        self._config = ConfigParser()
        self._add_commandline_arguments(cli_conf)
        self._read_proxy_default_config()

        config_abs_path = os.path.abspath(cli_conf.config_path)

        try:
            self._config.read(config_abs_path)[0]
        except IndexError:
            logger.warning("Configuration file '%s' could not be read... "
                           "Using ONLY default settings", config_abs_path)
        else:
            logger.debug("Using configuration from '%s'", config_abs_path)

        # include configuration for all modifiers
        self._read_modifiers_default_config()

    def _read_modifiers_default_config(self):
        """

        :return:
        """
        for mod_name in self.getlist(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_MODIFIERS):
            modifier = get_modifier_by_name(mod_name)
            if not modifier:
                logger.error("Error in Modifiers configuration!")
                raise BrokenDNSProxyError("Modifier with name '{0}' doesn't exist!".format(mod_name))
            BrokenDnsProxyConfiguration.config_parser_read_dict(self._config, {modifier.config_section_name():
                                                                               modifier.default_configuration_dict()})

    def _read_proxy_default_config(self):
        """
        Read the default configuration of BDP and add it to Config

        :return: None
        """
        BrokenDnsProxyConfiguration.config_parser_read_dict(self._config, {GlobalConfig.config_section_name():
                                                                           GlobalConfig.default_configuration_dict()})

    def _add_commandline_arguments(self, cli_conf):
        """
        Construct a dict from CLI arguments and add it to Config

        :param cli_conf: ArgumentParser object initialized by CLI args
        :return: None
        """
        cli_settings = {GlobalConfig.config_section_name(): {
            GlobalConfig.CONFIG_VERBOSE: 'yes' if cli_conf.verbose else 'no',
            GlobalConfig.CONFIG_CONFIG_PATH: os.path.abspath(cli_conf.config_path)
        }}

        BrokenDnsProxyConfiguration.config_parser_read_dict(self._config, cli_settings)

    def __getattr__(self, name):
        """
        Forward all ConfigParser attributes to ConfigParser object

        :param name: name of the attribute
        :return: returns the selected attribute
        """
        try:
            return getattr(self._config, name)
        except AttributeError:
            return object.__getattribute__(self, name)

    def getlist(self, section, option):
        """
        Get the particular section -> option -> value as a list
        Values has to be separated using whitespace.

        :param section: existing section
        :param option: existing option
        :return: list of values or exception on error
        """
        value = self.get(section, option)
        return value.split()

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