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
import threading
import signal
import json
import requests

from cloudflare_ddns.core.exceptions import ImproperlyConfigured
from cloudflare_ddns.utils.ips import get_cf_ipv4, get_cf_ipv6, get_ipv4_address
from cloudflare_ddns.conf import settings

log = logging.getLogger('cf_logging')


class Cloudflare(object):

    endpoint = getattr(settings, 'CLOUDFLARE_ZONE_QUERY_API')

    def __init__(self, **kwargs):
        kw_auth_type = kwargs.get('auth_type', getattr(settings, 'CF_AUTH_TYPE'))

        kw_email = kwargs.get('email', getattr(settings, 'CF_EMAIL'))
        kw_api_key = kwargs.get('api_key', getattr(settings, 'CF_API_KEY'))
        kw_api_token = kwargs.get('api_token', getattr(settings, 'CF_API_TOKEN'))

        if kw_auth_type == 'token':
            bearer = str("Bearer " + kw_api_token)
            self.headers = {
                'Authorization': bearer,
                'Content-Type': 'application/json'
            }
        elif kw_auth_type == 'key':
            if kw_email and kw_api_key:
                self.headers = {
                    'X-Auth-Email': kw_email,
                    'X-Auth-Key': kw_api_key,
                    'Content-Type': 'application/json'
                }
            else:
                raise ImproperlyConfigured("The email for api key is missing from configuration")

        self.kill_now = threading.Event()
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def __call__(self, zone, record, ttl, proxied):
        zone_id = self.zones(zone)['result'][0]['id']
        record_id = self.dns_records(zone_id, record)['result'][0]['id']
        ip_address = get_cf_ipv6()
        if ip_address != self.dns_records(zone_id, record)['result'][0]['content']:
            return self.update_record(zone_id, record_id, record, ttl, ip_address, proxied)
        else:
            return "Record is up-to-date"

    def exit_gracefully(self, signum, frame):
        print("🛑 Stopping main thread...")
        self.kill_now.set()

    def get_user(self):
        """The currently logged in/authenticated User

        :return:
        """
        r = requests.get(self.endpoint + "/user", headers=self.headers)
        return r.json()

    def zones(self, zone):
        """Query Cloudflare zones(domains) to find out more information about that zone

        A Zone is a domain name along with its subdomains and other identities

        :param zone: name of the zone, or domain name
        :return:
        """
        payload = {'name': zone}
        r = requests.get(self.endpoint + "/zones", headers=self.headers, params=payload)
        return r.json()

    def dns_records(self, zone_id, record):
        payload = {'name': record}
        r = requests.get(self.endpoint + "/zones/" + zone_id + "/dns_records", headers=self.headers, params=payload)
        return r.json()

    def update_record(self, zone_id, record_id, record, ttl, ip_address, proxied):
        """

        :param zone_id:
        :param record_id:
        :param record:
        :param ttl:
        :param ip_address:
        :param proxied:
        :return:
        """
        payload = {'type': 'AAAA', 'name': record, 'ttl': int(ttl), 'content': ip_address, 'proxied': bool(proxied)}
        r = requests.put(self.endpoint + "/zones/" + zone_id + "/dns_records/" + record_id, headers=self.headers,
                         data=json.dumps(payload))
        return r.json()
