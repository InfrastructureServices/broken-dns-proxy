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

from broken_dns_proxy.exceptions import BrokenDNSProxyError


modifiers = {}


def register_modifier(modifier):
    if is_modifier(modifier.config_section_name().lower()):
        raise BrokenDNSProxyError("Modifier with name {0} already exists!".format(modifier.config_section_name()))
    modifiers[modifier.config_section_name().lower()] = modifier
    return modifier


def is_modifier(modifier_name):
    return True if get_modifier_by_name(modifier_name) else False


def get_modifier_by_name(modifier_name):
    try:
        return modifiers[modifier_name.lower()]
    except KeyError:
        return None