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

import os
import argparse
from importlib import import_module


def load_arguments():
    """Load arguments used in shell instance

    :return: An objects with argument name properties
    """
    parser = argparse.ArgumentParser(description="Using Cloudflare service you can update the A and AAAA records "
                                                 "automatically and use this feature as a Dynamic DNS")
    parser.add_argument('-r', '--repeat', type=int, help="Repeat the script using specified time or default time",
                        default=5 * 60)
    parser.add_argument('--configure', action='store_true',
                        help='Interactively configure the account and domain for the DDNS updates.')
    parser.add_argument('--update-now', action='store_true', help='Update DNS records right now.')

    parser.add_argument("-d", "--debug", action='store_true', help="Debug the running application")

    parser.add_argument("--cf-domains", type=str, help="Cloudflare domains that the A or AAAA records will be updated")
    parser.add_argument("--cf-email", type=str, help="Set the Cloudflare email"),
    parser.add_argument('--cf-auth-type', type=str, help='Cloudflare API auth type. token or key')
    parser.add_argument('--cf-api-token', type=str, help='Cloudflare API auth token')
    parser.add_argument('--cf-api-key', type=str, help='Cloudflare API auth key')
    parser.add_argument('--cf-ipv6', action='store_true', help='Update only AAAA DNS records')
    parser.add_argument('--cf-ipv4', action='store_true', help='Update only A DNS records')

    return parser.parse_args()


def import_string(dotted_path):
    """ Import a dotted module path and return the attribute/class designated by the
        last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
                          ) from err



