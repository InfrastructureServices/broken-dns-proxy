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

import logging


class LoggerHelper(object):
    """
    Helper class for setting up a logger
    """

    @staticmethod
    def get_basic_logger(logger_name, level=logging.DEBUG):
        """
        Sets-up a basic logger without any handler

        :param logger_name: Logger name
        :param level: severity level
        :return: created logger
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        return logger

    @staticmethod
    def add_stream_handler(logger, level=None):
        """
        Adds console handler with given severity.

        :param logger: logger object to add the handler to
        :param level: severity level
        :return: None
        """
        console_handler = logging.StreamHandler()
        if level:
            console_handler.setLevel(level)
        logger.addHandler(console_handler)

    @staticmethod
    def add_file_handler(logger, path, formatter=None, level=None):
        """
        Adds FileHandler to a given logger

        :param logger: Logger object to which the file handler will be added
        :param path: Path to file where the debug log will be written
        :return: None
        """
        file_handler = logging.FileHandler(path, 'w')
        if level:
            file_handler.setLevel(level)
        if formatter:
            file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


#  the main Broken DNS Proxy logger
logger = LoggerHelper.get_basic_logger('broken-dns-proxy')
