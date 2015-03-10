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
import dns.message
import struct

from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.logger import logger


class Client(object):
    """
    Class representing a client connection
    """

    _client_sock = None
    _client_addr = None
    _client_msg_len = None
    _client_msg_raw = ''
    _client_msg = None

    def __init__(self, server_socket):
        """
        Constructor

        :param server_socket: The socket object on which we have possible client pending
        :return: None
        """
        if server_socket.type not in (socket.SOCK_DGRAM, socket.SOCK_STREAM):
            raise BrokenDNSProxyError("Pending client on socket with wrong type '{0}'".format(server_socket.type))

        self._receive_client_msg(server_socket)
        self._client_msg = dns.message.from_wire(self._client_msg_raw)
        logger.debug("Received DNS message:\n"
                     "-----------------------------\n"
                     "%s\n"
                     "-----------------------------", str(self._client_msg))

    def _receive_client_msg(self, server_socket):
        """

        :param server_socket:
        :return:
        """
        if server_socket.type == socket.SOCK_STREAM:
            self._handle_stream_socket(server_socket)
        elif server_socket.type == socket.SOCK_DGRAM:
            self._handle_datagram_socket(server_socket)

    def _handle_stream_socket(self, server_socket):
        """

        :param server_socket:
        :return:
        """
        self._client_sock, self._client_addr = server_socket.accept()
        logger.debug('TCP client {0} connected'.format(self._client_addr))

        self._client_msg_len = struct.unpack('!H', self._client_sock.recv(2))[0]
        logger.debug('TCP Query of length {0}'.format(self._client_msg_len))

        while len(self._client_msg_raw) < self._client_msg_len:
            # read all data
            chunk = self._client_sock.recv(self._client_msg_len - len(self._client_msg_raw))
            if not chunk:
                raise BrokenDNSProxyError('Unable to get all TCP data')
            self._client_msg_raw += chunk

    def _handle_datagram_socket(self, server_socket):
        """

        :param server_socket:
        :return:
        """
        # 16bit max udp length limit
        self._client_msg_raw, self._client_addr = server_socket.recvfrom(2**16)
        logger.debug('Received UDP data from: {0}'.format(self._client_addr))
        self._client_msg_len = len(self._client_msg_raw)
        logger.debug('UDP Query of length {0}'.format(self._client_msg_len))
        self._client_sock = server_socket

    def msg(self):
        """
        Returns the DNS Message object with the client query

        :return: DNS Message object with the client Query
        """
        return self._client_msg

    def send(self, msg):
        """
        Send the msg as a response to the client query.

        :param msg: DNS Message object
        :return: None
        """
        logger.debug('Sending message to client %s:\n'
                     '-----------------------------\n'
                     '%s\n'
                     '-----------------------------',
                     str(self._client_addr), str(msg))

        if self._client_sock.type == socket.SOCK_STREAM:
            self._send_stream(msg)
        elif self._client_sock.type == socket.SOCK_DGRAM:
            self._send_datagram(msg)

    def _send_stream(self, msg):
        """
        Send DNS Message to client connected using TCP

        :param msg: DNS Message object to sent to the client
        :return: None
        """
        # to make sure the Response ID matches the Query ID
        msg.id = self._client_msg.id
        msg_raw = msg.to_wire()
        msg_len = struct.pack('!H', len(msg_raw))

        # send the data to the client. 1st 2B is the length
        self._client_sock.send(msg_len + msg_raw)

    def _send_datagram(self, msg):
        """
        Send DNS Message to client connected using UDP

        :param msg: DNS Message object to send to the client
        :return: None
        """
        # to make sure the Response ID matches the Query ID
        msg.id = self._client_msg.id
        msg_raw = msg.to_wire()

        # send the data to the client
        self._client_sock.sendto(msg_raw, self._client_addr)
