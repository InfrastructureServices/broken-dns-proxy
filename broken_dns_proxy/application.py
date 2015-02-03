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


class Application(object):

    def __init__(self, cli_args=None):
        """
        """
        self._cli_args = cli_args

        if self._cli_args.verbose:
            LoggerHelper.add_stream_handler(logger, logging.DEBUG)
        else:
            LoggerHelper.add_stream_handler(logger, logging.INFO)
        self._add_debug_log_file()
        self._server = ProxyServer(53535)

    def _add_debug_log_file(self):
        """
        Add the application wide debug log file
        :return:
        """
        debug_log_file = os.path.join(os.getcwd(), 'broken-dns-proxy-debug.log')
        try:
            LoggerHelper.add_file_handler(logger,
                                          debug_log_file,
                                          logging.Formatter("%(asctime)s %(levelname)s\t%(filename)s"
                                                            ":%(lineno)s %(funcName)s: %(message)s"),
                                          logging.DEBUG)
        except (IOError, OSError):
            logger.warning("Can not create debug log '{0}'".format(debug_log_file))
        else:
            self.debug_log_file = debug_log_file

    def run(self):
        self._server.process()
