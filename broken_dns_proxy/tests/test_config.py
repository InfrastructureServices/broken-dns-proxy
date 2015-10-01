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


import os

from broken_dns_proxy.arguments_parser import ArgumentsParser
from broken_dns_proxy.config import BrokenDnsProxyConfiguration
from broken_dns_proxy.config_common import GlobalConfig
from broken_dns_proxy.modifiers import FlagsModifier


class TestBrokenDnsProxyConfiguration(object):
    """
    Test cases for BrokenDnsProxyConfiguration class
    """

    def test_default_configuration(self):
        """
        Test the default configuration without CLI arguments.
        """
        cli = ArgumentsParser('')
        config = BrokenDnsProxyConfiguration(cli)

        assert config._config.has_section(GlobalConfig.config_section_name())
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_VERBOSE)
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_CONFIG_PATH)
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_PORT)
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_ADDRESS)
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_ADDRESS)
        assert config._config.has_option(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_MODIFIERS)

        # there is no Modifier specific configuration
        assert not config._config.has_section(FlagsModifier.config_section_name())

    def test_configuration_with_flags_modifier(self):
        """
        Test that adding FlagsModifier into modifiers option will include the modifier default configuration
        """
        cfg_file = os.path.abspath('broken_dns_proxy/tests/testing_files/config_with_modifier')
        cli = ArgumentsParser(['-c', cfg_file])
        config = BrokenDnsProxyConfiguration(cli)

        assert config._config.has_section(FlagsModifier.config_section_name())
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_AA)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_TC)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_RD)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_RA)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_AD)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_CD)
        assert config._config.has_option(FlagsModifier.config_section_name(), FlagsModifier.CONFIG_DO)


