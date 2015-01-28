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

import dns
import dns.flags
import re

from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.logger import logger


def _control_flags_text(text_flags):
    """
    function control if flags in text are on list of flags
    :param text_flags:
    :return:
    """
    if not re.match('^(AA|AD|CD|QR|RA|RD|TC|\s)*$', text_flags, flags=re.IGNORECASE):
        raise BrokenDNSProxyError("Set wrong flags in message")
    else:
        return True


def _control_one_flag_text(text_flag):
    """
    function control if flag in text is on list of flags
    :param text_flag:
    :return:
    """
    if not re.match('\s*(AA|AD|CD|QR|RA|TC)\s*', text_flag, flags=re.IGNORECASE):
        raise BrokenDNSProxyError("Wrong set flag or set more flags than one")
    else:
        return True


class Modifier(object):
    """
        Class for change data in message
    """

    _modifier_msg = None

    def __init__(self, message):
        """ """
        self._modifier_msg = message

    def set_new_flags(self, flags_in_text):
        """
        set new flags in message from text string
            'AA', 'AD','CD','QR','RA','RD','TC'
         example set_flags("AA RD CD")

        :param flags_in_text:
        :return:
        """
        if _control_flags_text(flags_in_text):
            self._modifier_msg.flags = dns.flags.from_text(flags_in_text)
            logger.info("Flags: {0}".format(dns.flags.to_text(self._modifier_msg.flags)))

    def add_flags(self, flags_in_text):
        """
        add new flags to list of actual flags in message
        :param flags_in_text:
        :return:
        """
        if _control_flags_text(flags_in_text):
            flags = dns.flags.to_text(self._modifier_msg.flags)
            new = flags+" "+flags_in_text
            self._modifier_msg.flags=dns.flags.from_text(new)
            logger.info("Flags: {0}".format(dns.flags.to_text(self._modifier_msg.flags)))

    def remove_one_flag(self, flag_in_text):
        """
        remove ONE flag from list of flags in message
        :param flag_in_text:
        :return:
        """
        if _control_one_flag_text(flag_in_text):
            flags = dns.flags.to_text(self._modifier_msg.flags)
            new = flags.replace(flag_in_text, "")
            self._modifier_msg.flags = dns.flags.from_text(new)
            logger.info("Flags: {0}".format(dns.flags.to_text(self._modifier_msg.flags)))










