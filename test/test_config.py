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

from broken_dns_proxy.arguments_parser import ArgumentsParser
from broken_dns_proxy.config import BrokenDnsProxyConfiguration
from broken_dns_proxy.proxy_server import ProxyServer


class TestBrokenDnsProxyConfiguration(object):
    """
    Test cases for BrokenDnsProxyConfiguration class
    """

    def test_default_configuration(self):
        """
        Test the default configuration without CLI arguments.

        :return:
        """
        cli = ArgumentsParser('')
        config = BrokenDnsProxyConfiguration(cli)

        assert config._config.has_section(ProxyServer.config_section_name())
        assert config._config.has_option(ProxyServer.config_section_name(), 'Verbose')
        assert config._config.has_option(ProxyServer.config_section_name(), 'ConfigPath')
        assert config._config.has_option(ProxyServer.config_section_name(), 'Port')
        assert config._config.has_option(ProxyServer.config_section_name(), 'Address')
        assert config._config.has_option(ProxyServer.config_section_name(), 'UpstreamServers')
        assert config._config.has_option(ProxyServer.config_section_name(), 'Modifiers')