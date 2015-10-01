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

import sys
import os

from broken_dns_proxy.arguments_parser import ArgumentsParser
from broken_dns_proxy.application import Application
from broken_dns_proxy.logger import logger, LoggerHelper, logging
from broken_dns_proxy.exceptions import BrokenDNSProxyError


def __main__():
    """
    Entry point for command line
    """
    try:
        # add application-wide debug log
        LoggerHelper.add_debug_log_file(os.getcwd())

        args = ArgumentsParser(sys.argv[1:])

        if args.verbose is True:
            LoggerHelper.add_stream_handler(logger,
                                            logging.Formatter('%(levelname)s:\t%(message)s'),
                                            logging.DEBUG)
        else:
            LoggerHelper.add_stream_handler(logger,
                                            logging.Formatter('%(levelname)s:\t%(message)s'),
                                            logging.INFO)

        app = Application(args)
        app.run()
    except KeyboardInterrupt:
        logger.info('Interrupted by user')
    except BrokenDNSProxyError as e:
        logger.error('%s', str(e))
        sys.exit(1)
    else:
        sys.exit(0)
    finally:
        logger.info('Exiting...')
