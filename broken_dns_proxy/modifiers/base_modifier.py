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

from broken_dns_proxy.config_common import ConfigurableClass


class BaseModifier(ConfigurableClass):
    """
    Base class for dns message modifier
    """

    def __init__(self, configuration):
        """
        Constructor

        :param configuration: BrokenDnsProxyConfiguration object
        :return: new object
        """
        raise NotImplementedError()

    def modify(self, dns_message):
        """
        Method modifying the DNS message, based on Modifier configuration

        :param dns_message: dns message object to modify
        :return: possibly modified dns message object
        """
        raise NotImplementedError()