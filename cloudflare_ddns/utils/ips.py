#  -*- coding: utf-8 -*-
#
#              Copyright (C) 2018-2021 ProGeek
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import ipaddress
import requests

from cloudflare_ddns.conf import settings
from cloudflare_ddns.core.exceptions import ValidationError

log = logging.getLogger('cf_logging')


def clean_ipv6_address(ip_str, unpack_ipv4=False,
                       error_message="This is not a valid IPv6 address."):
    """
    Clean an IPv6 address string.
    Raise ValidationError if the address is invalid.
    Replace the longest continuous zero-sequence with "::", remove leading
    zeroes, and make sure all hextets are lowercase.
    Args:
        ip_str: A valid IPv6 address.
        unpack_ipv4: if an IPv4-mapped address is found,
        return the plain IPv4 address (default=False).
        error_message: An error message used in the ValidationError.
    Return a compressed IPv6 address or the same value.
    """
    try:
        addr = ipaddress.IPv6Address(int(ipaddress.IPv6Address(ip_str)))
    except ValueError:
        raise ValidationError(error_message, code='invalid')

    if unpack_ipv4 and addr.ipv4_mapped:
        return str(addr.ipv4_mapped)
    elif addr.ipv4_mapped:
        return '::ffff:%s' % str(addr.ipv4_mapped)

    return str(addr)


def is_valid_ipv6_address(ip_str):
    """
    Return whether or not the `ip_str` string is a valid IPv6 address.
    """
    try:
        ipaddress.IPv6Address(ip_str)
    except ValueError:
        return False
    return True


def get_cf_ipv4():
    """Get from Cloudflare service the IPv4 address of local host

    :return:
    """
    a = None

    try:
        log.info("Fetching IPv4 IP from: {}".format(settings.EXTERNAL_CF_IPV4_QUERY_API))
        a = requests.get(settings.EXTERNAL_CF_IPV4_QUERY_API, timeout=10).text.split("\n")
        a.pop()
        a = dict(s.split("=") for s in a)['ip']  # noqa
    except requests.exceptions.RequestException as e:
        pass
        log.error("🧩 Cloudflare IPv4 not detected")

    return a


def get_cf_ipv6():
    """Get from Cloudflare service the IPv6 address of local host

    :return:
    """
    aaaa = None  # noqa

    try:
        log.info("Fetching IPv6 IP from: {}".format(settings.EXTERNAL_CF_IPV6_QUERY_API))
        aaaa = requests.get(settings.EXTERNAL_CF_IPV6_QUERY_API, timeout=10).text.split("\n")
        aaaa.pop()
        aaaa = dict(s.split("=") for s in aaaa)['ip']  # noqa
    except requests.exceptions.RequestException as e:
        log.error("🧩 Cloudflare IPv6 not detected")

    return aaaa


def get_ipv4_address():
    """

    :return:
    """

    for api in settings.EXTERNAL_IPV4_QUERY_APIS:
        try:
            log.info("Fetching {}".format(api))
            r = requests.get(api, timeout=10)
            return r.text.strip()  # Fix bug with trailing whitespace
        except requests.exceptions.RequestException as e:
            log.error('Cannot fetch your external ip. {} not reachable.'.format(api))

    return None
