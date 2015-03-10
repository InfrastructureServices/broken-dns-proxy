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

from broken_dns_proxy.modifiers import get_modifier_by_name
from broken_dns_proxy.logger import logger
from broken_dns_proxy.exceptions import BrokenDNSProxyError
from broken_dns_proxy.config_common import GlobalConfig


class ModificationChain(object):
    """
    Class representing a specific chain od modifiers
    """

    def __init__(self, configuration):
        """

        :param configuration:
        :return:
        """
        self._modifiers = list()
        modifiers_list = configuration.getlist(GlobalConfig.config_section_name(), GlobalConfig.CONFIG_MODIFIERS)

        for mod_name in modifiers_list:
            mod = get_modifier_by_name(mod_name)
            if not mod:
                raise BrokenDNSProxyError("Modifier '{0}' does not exist!".format(mod_name))
            logger.debug("Adding modifier '%s' to Modification Chain", mod_name)
            self._modifiers.append(mod(configuration))

    def run_modifiers(self, dns_message):
        """

        :param dns_message:
        :return:
        """
        logger.debug("Running total '%d' modifiers...", len(self._modifiers))

        for mod in self._modifiers:
            logger.debug("Running '%s' modifier...", mod.config_section_name())
            dns_message = mod.modify(dns_message)

        return dns_message