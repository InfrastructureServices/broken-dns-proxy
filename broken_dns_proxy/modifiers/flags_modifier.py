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

import dns.flags

from broken_dns_proxy.modifiers import register_modifier
from broken_dns_proxy.modifiers import BaseModifier
from broken_dns_proxy.logger import logger


@register_modifier
class FlagsModifier(BaseModifier):
    """
    Modifier modifying DNS Header and EDNS header flags.
    Default configuration is to NOT change any of the flags.

    DNS Header flags
        Bit   Flag     Description      Reference
        bit 5   AA  Authoritative Answer [RFC 1035]
        bit 6   TC  Truncated Response   [RFC 1035]
        bit 7   RD  Recursion Desired    [RFC 1035]
        bit 8   RA  Recursion Allowed    [RFC 1035]
        bit 9       Reserved
        bit 10  AD  Authentic Data       [RFC 4035]
        bit 11  CD  Checking Disabled    [RFC 4035]

    EDNS Header flags
        Bit    Flag   Description        Reference
        Bit 0     DO  DNSSEC answer OK [RFC 4035][RFC 3225]
        Bit 1-15      Reserved
    """

    ACTION_SET = True
    ACTION_CLEAR = False
    ACTION_NONE = 'unchanged'

    CONFIG_SECTION_NAME = 'FlagsModifier'
    # DNS header flags
    CONFIG_AA = 'AA'
    CONFIG_TC = 'TC'
    CONFIG_RD = 'RD'
    CONFIG_RA = 'RA'
    CONFIG_AD = 'AD'
    CONFIG_CD = 'CD'
    # EDNS header flags
    CONFIG_DO = 'DO'

    CONFIG_AA_VALUE = \
        CONFIG_TC_VALUE = \
        CONFIG_RD_VALUE = \
        CONFIG_RA_VALUE = \
        CONFIG_AD_VALUE = \
        CONFIG_CD_VALUE = \
        CONFIG_DO_VALUE = ACTION_NONE

    _options_dict = {
        CONFIG_AA: CONFIG_AA_VALUE,
        CONFIG_TC: CONFIG_TC_VALUE,
        CONFIG_RD: CONFIG_RD_VALUE,
        CONFIG_RA: CONFIG_RA_VALUE,
        CONFIG_AD: CONFIG_AD_VALUE,
        CONFIG_CD: CONFIG_CD_VALUE,
        CONFIG_DO: CONFIG_DO_VALUE
    }

    def __init__(self, configuration):
        """
        Constructor

        :param configuration: BrokenDnsProxyConfiguration object
        :return: new object
        """
        # global configuration
        self._configuration = configuration
        # ProxyServer specific configuration
        self._aa_flag = self._get_action(self.CONFIG_AA)
        self._tc_flag = self._get_action(self.CONFIG_TC)
        self._rd_flag = self._get_action(self.CONFIG_RD)
        self._ra_flag = self._get_action(self.CONFIG_RA)
        self._ad_flag = self._get_action(self.CONFIG_AD)
        self._cd_flag = self._get_action(self.CONFIG_CD)
        self._do_flag = self._get_action(self.CONFIG_DO)

    def _get_action(self, option_name):
        """
        Get the action for a specific option (flag)

        :param option_name: option name
        :return: True for set; False for clear/unset; None for unchanged
        """
        try:
            return self._configuration.getboolean(self.CONFIG_SECTION_NAME, option_name)
        except ValueError:
            value = self._configuration.get(self.CONFIG_SECTION_NAME, option_name)
            if value.strip().lower() != self.ACTION_NONE:
                logger.error("Wrong value '{0}' in configuration for {1}", value, option_name)

    def modify(self, dns_message):
        """
        Method modifying the DNS message, based on Modifier configuration

        :param dns_message: dns message object to modify
        :return: possibly modified dns message object
        """
        # go through all flags in settings and set/clear/do nothing with the flag
        # AA  Authoritative Answer [RFC 1035]
        if self._aa_flag is not None:
            if self._aa_flag:
                logger.debug("Setting AA flag")
                dns_message.flags |= dns.flags.AA
            else:
                logger.debug("Clearing AA flag")
                dns_message.flags &= ~dns.flags.AA
        # TC  Truncated Response   [RFC 1035]
        if self._tc_flag is not None:
            if self._tc_flag:
                logger.debug("Setting TC flag")
                dns_message.flags |= dns.flags.TC
            else:
                logger.debug("Clearing TC flag")
                dns_message.flags &= ~dns.flags.TC
        # RD  Recursion Desired    [RFC 1035]
        if self._rd_flag is not None:
            if self._rd_flag:
                logger.debug("Setting RD flag")
                dns_message.flags |= dns.flags.RD
            else:
                logger.debug("Clearing RD flag")
                dns_message.flags &= ~dns.flags.RD
        # RA  Recursion Allowed    [RFC 1035]
        if self._ra_flag is not None:
            if self._ra_flag:
                logger.debug("Setting RA flag")
                dns_message.flags |= dns.flags.RA
            else:
                logger.debug("Clearing RA flag")
                dns_message.flags &= ~dns.flags.RA
        # AD  Authentic Data       [RFC 4035]
        if self._ad_flag is not None:
            if self._ad_flag:
                logger.debug("Setting AD flag")
                dns_message.flags |= dns.flags.AD
            else:
                logger.debug("Clearing AD flag")
                dns_message.flags &= ~dns.flags.AD
        # CD  Checking Disabled    [RFC 4035]
        if self._cd_flag is not None:
            if self._cd_flag:
                logger.debug("Setting CD flag")
                dns_message.flags |= dns.flags.CD
            else:
                logger.debug("Clearing CD flag")
                dns_message.flags &= ~dns.flags.CD
        # DO  DNSSEC answer OK [RFC 4035][RFC 3225]
        if self._do_flag is not None:
            if self._do_flag:
                # enable EDNS if not enabled
                if dns_message.edns == -1:
                    logger.debug("EDNS0 not used... enabling")
                    dns.message.use_edns()
                logger.debug("Setting DO flag")
                dns_message.ednsflags |= dns.flags.DO
            else:
                logger.debug("Clearing DO flag")
                dns_message.ednsflags &= ~dns.flags.DO
