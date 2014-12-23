# -*- coding: utf-8 -*-
#
# Simple DNS Proxy for simulating DNS issues
# Copyright (C) 2014  Red Hat, Inc.
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
import binascii
import dns.message

from broken_dns_proxy.logger import logger
from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.client import Client


class ProxyServer(object):
    """
    Class representing the proxy server listening on ports for client Queries.
    """

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

                    # s_udp.sendto(data, addr)  # it doesnt work
                    # rrset = msg.answer
                    #for r in rrset:
                    #    if r.name in zones:
                    #        print r.name, 'NOTIFY'

        finally:
            for s in self._sockets:
                s.close()