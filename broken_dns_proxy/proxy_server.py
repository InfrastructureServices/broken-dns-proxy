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

import socket
import select

import dns.message
import dns.rcode
import dns.flags
import dns.query

from broken_dns_proxy.logger import logger
from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.client import Client
from broken_dns_proxy.modifiers.modifier import Modifier


class ProxyServer(object):
    """
    Class representing the proxy server listening on ports for client Queries.
    """

    # Some configuration values are reserved and not set here as
    # these are read from the command line. Reserved:
    # 'Verbose'
    # 'ConfigPath'

    CONFIG_SECTION_NAME = 'Proxy'
    CONFIG_DEFAULT_PORT = {'Port': 53}
    CONFIG_DEFAULT_ADDRESS = {'Address': 'localhost'}
    CONFIG_DEFAULT_UPSTREAM_SERVERS = {'UpstreamServers': '8.8.8.8 8.8.4.4'}
    CONFIG_DEFAULT_MODIFIERS = {'Modifiers': ''}

    @staticmethod
    def config_section_name():
        """
        Return the string with name of the configuration section for Proxy server

        :return: str
        """
        return ProxyServer.CONFIG_SECTION_NAME

    @staticmethod
    def default_configuration_dict():
        """

        :return:
        """
        config = dict()
        for d in (ProxyServer.CONFIG_DEFAULT_PORT, ProxyServer.CONFIG_DEFAULT_ADDRESS,
                  ProxyServer.CONFIG_DEFAULT_UPSTREAM_SERVERS, ProxyServer.CONFIG_DEFAULT_MODIFIERS):
            config.update(d)
        return config

    def __init__(self, port=53):
        """
        Initialize the proxy server object

        :param port: port on which the proxy should listen
        :return:
        """
        self._listen_port = port
        self._sockets = []

    def process(self):
        """
        Start listening and processing Queries.
        :return:
        """
        s_udp6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s_tcp6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s_udp6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sockets.append(s_udp6)
        self._sockets.append(s_tcp6)

        try:
            # kernel allows to receive IPv4 packets
            try:
                s_udp6.bind(('', self._listen_port))
                s_tcp6.bind(('', self._listen_port))
            except socket.error as e:
                # [Errno 13] Permission denied
                if e.errno == 13:
                    raise BrokenDNSProxyError('You need to be root to bind to port {0}'.format(self._listen_port))
                else:
                    raise BrokenDNSProxyError(e.strerror)

            s_tcp6.listen(0)

            logger.info('Listening on port {0}...'.format(self._listen_port))

            while True:
                ready_r, ready_w, _ = select.select(self._sockets, [], [])

                for s in ready_r:
                        client = Client(s)
                        msg = client.msg()
                        logger.info('Received MSG:')
                        logger.info(str(msg))

                        # sample code sending a response to the client
                        upstream_server = '8.8.8.8'
                        response = dns.query.udp(msg, upstream_server)

                        # sample code how modified msg
                        modifier = Modifier(response)
                        modifier.set_new_flags("qr aa ")
                        modifier.add_flags("tc rd DO do ")
                        modifier.remove_one_flag("tc")
                        modifier.remove_one_flag("do")

                        client.send(response)
        finally:
            for s in self._sockets:
                s.close()