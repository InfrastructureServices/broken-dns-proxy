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
import logging

from broken_dns_proxy.logger import logger, LoggerHelper
from broken_dns_proxy.proxy_server import ProxyServer
from broken_dns_proxy.config import BrokenDnsProxyConfiguration


class Application(object):

    def __init__(self, cli_args=None):
        """
        """
        self.configuration = BrokenDnsProxyConfiguration(cli_args)
        self._server = ProxyServer(self.configuration)

    def run(self):
        logger.debug("Staring proxy server '%s'", str(self._server))
        self._server.process()
