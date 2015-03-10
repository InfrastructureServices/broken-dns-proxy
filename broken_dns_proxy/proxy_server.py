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
import random

import dns.message
import dns.rcode
import dns.flags
import dns.query

from broken_dns_proxy.logger import logger
from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.client import Client
from broken_dns_proxy.modifiers import ModificationChain
from broken_dns_proxy.config_common import GlobalConfig


class ProxyServer(object):
    """
    Class representing the proxy server listening on ports for client Queries.
    """

    def __init__(self, configuration):
        """
        Initialize the proxy server object

        :param port: port on which the proxy should listen
        :return:
        """
        # global configuration
        self._configuration = configuration
        # ProxyServer specific configuration
        self._listen_port = self._configuration.getint(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_PORT)
        self._listen_address = self._configuration.get(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_ADDRESS)
        self._upstream_servers = self._configuration.getlist(GlobalConfig.config_section_name(),
                                                             GlobalConfig.CONFIG_UPSTREAM_SERVERS)
        # internal variables
        self._sockets = []
        # create Modification chain
        self._modification_chain = ModificationChain(self._configuration)

    def __str__(self):
        """

        :return:
        """
        return "<ProxyServer address='{0}' port='{1}' upstream_servers='{2}'>".format(self._listen_address,
                                                                                      self._listen_port,
                                                                                      self._upstream_servers)

    def process(self):
        """
        Start listening and processing Queries.
        :return:
        """
        # TODO: need to figure out what to do when ony IPv4 address is to be used
        s_udp6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s_tcp6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s_udp6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sockets.append(s_udp6)
        self._sockets.append(s_tcp6)

        try:
            # kernel allows to receive IPv4 packets
            try:
                s_udp6.bind((self._listen_address, self._listen_port))
                s_tcp6.bind((self._listen_address, self._listen_port))
            except socket.error as e:
                # [Errno 13] Permission denied
                if e.errno == 13:
                    logger.error('You need to be root to bind to port {0}'.format(self._listen_port))
                # [Errno -9] Address family for hostname not supported
                elif e.errno == -9:
                    logger.error("Only IPv4 addresses or 'localhost' is supported at this point.")
                raise BrokenDNSProxyError(e.strerror)

            s_tcp6.listen(0)

            logger.info('Listening on port {0}...'.format(self._listen_port))

            while True:
                ready_r, ready_w, _ = select.select(self._sockets, [], [])

                for s in ready_r:
                    client = Client(s)
                    msg = client.msg()

                    # sample code sending a response to the client
                    upstream_server = random.choice(self._upstream_servers)
                    logger.debug("Forwarding Query to upstream server '{0}'".format(upstream_server))
                    response = dns.query.udp(msg, upstream_server)

                    # modify the message for client
                    self._modification_chain.run_modifiers(response)

                    client.send(response)
        finally:
            for s in self._sockets:
                s.close()