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

import dns
import dns.flags
import re

from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.logger import logger


def _control_flags_text(text_flags):
    """
    function control if flags in text are on list of flags
    :param text_flags:
    :return: true or error
    """
    if not re.match('^(AA|AD|CD|QR|RA|RD|TC|DO|\s)*$', text_flags, flags=re.IGNORECASE):
        raise BrokenDNSProxyError("Set wrong flags in message")
    else:
        return True


def _control_one_flag_text(text_flag):
    """
    function control if flag in text is on list of flags
    :param text_flag:
    :return: true or error
    """
    if not re.match('\s*(AA|AD|CD|QR|RA|TC|DO)\s*', text_flag, flags=re.IGNORECASE):
        raise BrokenDNSProxyError("Wrong set flag or set more flags than one")
    else:
        return True


def _control_edns(text_flags):
    """
    control set of DO flag - because DO has special function to set it
    :param text_flags: flags we want to set
    :return: true/false if the DO flags in in text_flags
    """
    if re.match('.*DO.*', text_flags, flags=re.IGNORECASE):
        return True
    else:
        return False


def _rmv_edns_text(text_flags):
    """
    remove DO flags from text, because DO set the different way
    :param text_flags: lags we want to set
    :return new flags : string of flags without DO
    """
    text_flags = text_flags.upper()
    new_flags = text_flags.replace("DO", "")
    return new_flags


class Modifier(object):
    """
        Class for change data in message
    """

    _modifier_msg = None

    def __init__(self, message):
        """ """
        self._modifier_msg = message

    def _set_edns_flag(self, set):
        """
         this method set or unset the DO flag
         DO is set by different method from others flags
        :param set: true or false if we want or dont want set DO flag
        :return:
        """
        if set:
            self._modifier_msg.ednsflags = dns.flags.edns_from_text("DO")
        else:
            self._modifier_msg.ednsflags = dns.flags.edns_from_text(" ")

    def log_flags(self):
        logger.info("Flags:{0}".format(dns.flags.to_text(self._modifier_msg.flags)))
        logger.info("Flag edns :{0}".format(dns.flags.edns_to_text(self._modifier_msg.ednsflags)))

    def set_new_flags(self, flags_in_text):
        """
        set new flags in message from text string
            'AA', 'AD','CD','QR','RA','RD','TC', 'DO'
         example set_flags("AA RD CD")
        :param flags_in_text: text of flags we want to set
        :return:
        """
        if _control_flags_text(flags_in_text):
            if _control_edns(flags_in_text):
                flags_in_text = _rmv_edns_text(flags_in_text)
                self._set_edns_flag(True)
            self._modifier_msg.flags = dns.flags.from_text(flags_in_text)
            self.log_flags()

    def add_flags(self, flags_in_text):
        """
        add new flags to list of actual flags in message
        'AA', 'AD','CD','QR','RA','RD','TC', 'DO'
        :param flags_in_text: text of flags we want to add to flags
        :return:
        """
        if _control_flags_text(flags_in_text):
            if _control_edns(flags_in_text):
                flags_in_text = _rmv_edns_text(flags_in_text)
                self._set_edns_flag(True)
            flags = dns.flags.to_text(self._modifier_msg.flags)
            new = flags+" "+flags_in_text
            self._modifier_msg.flags = dns.flags.from_text(new)
            self.log_flags()

    def remove_one_flag(self, flag_in_text):
        """
        remove ONE flag from list of flags in message
        'AA', 'AD','CD','QR','RA','RD','TC', 'DO'
        :param flag_in_text: text of ONE flag we want to remove
        :return:
        """
        if _control_one_flag_text(flag_in_text):
            if _control_edns(flag_in_text):
                self._set_edns_flag(False)
            else:
                flags = dns.flags.to_text(self._modifier_msg.flags)
                flag_in_text = flag_in_text.upper()
                flags = flags.replace(flag_in_text, "")
                self._modifier_msg.flags = dns.flags.from_text(flags)
            self.log_flags()

    def enable_edns(self, version):

        self._modifier_msg.edns = version

    def disable_edns(self):
        self._modifier_msg.edns = -1








