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

from typing import Optional

import tld

from cloudflare_ddns.core.exceptions import ImproperlyConfigured
from cloudflare_ddns.utils.ips import get_cf_ipv4, get_cf_ipv6, get_ipv4_address
from cloudflare_ddns.conf import settings

log = logging.getLogger('cf_logging')


class GracefulExit:
    def __init__(self):
        self.kill_now = threading.Event()
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("🛑 Stopping main thread...")
        self.kill_now.set()


class Cloudflare(object):

    endpoint = getattr(settings, 'CLOUDFLARE_ENDPOINT_API')

    def __init__(self, **kwargs):
        kw_auth_type = kwargs.get('auth_type', getattr(settings, 'CF_AUTH_TYPE'))

        kw_email = kwargs.get('email', getattr(settings, 'CF_EMAIL'))
        kw_api_key = kwargs.get('api_key', getattr(settings, 'CF_API_KEY'))
        kw_api_token = kwargs.get('api_token', getattr(settings, 'CF_API_TOKEN'))

        if kw_auth_type == 'token':
            bearer = str("Bearer " + kw_api_token)
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': bearer
            }
        elif kw_auth_type == 'key':
            if kw_email and kw_api_key:
                self.headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Email': kw_email,
                    'X-Auth-Key': kw_api_key
                }
            else:
                raise ImproperlyConfigured("The email for api key is missing from configuration")

    # def __call__(self, zone, record, ttl, proxied):
    #     zone_id = self.zones(zone)['result'][0]['id']
    #     record_id = self.dns_records(zone_id, record)['result'][0]['id']
    #     ip_address = get_cf_ipv6()
    #     if ip_address != self.dns_records(zone_id, record)['result'][0]['content']:
    #         return self.update_record(zone_id, record_id, record, ttl, ip_address, proxied)
    #     else:
    #         return "Record is up-to-date"

    def query_api(self, endpoint, method: str = "GET", json_body=None, params=None, cur_page: int = 1,
                  timeout: float = 6.0):
        """Primary method to query the Cloudflare API

        :param params:
        :param endpoint:
        :param method: default method for request is GET
        :param json_body:
        :param cur_page
        :param timeout
        :return:
        """

        dft_params = {}

        if params and method == 'GET':
            dft_params = {'per_page': 50, 'page': cur_page}
            dft_params.update(params)

        response = requests.request(
            method=method,
            url=endpoint,
            headers=self.headers,
            timeout=timeout,
            json=json_body,
            params=dft_params
        )

        if response.ok:
            return response.json()
        else:
            log.error("📈 Error sending '" + method + "' request to '" + response.url + "': " + response.text)
            errors = [x.get("message") for x in response.json().get("errors")]
            for e in [x for x in errors if x]:
                log.error(e)
            return None

    def get_user(self):
        """The currently logged in/authenticated User

        :return:
        """
        return self.query_api(getattr(settings, "CLOUDFLARE_USER_API"))

    def get_zones_ids(self, zone=None):
        """Get zone id for all the zones present on the Cloudflare account
        Or you can get only a specific zone id using zone param

        A Zone is a domain name along with its subdomains and other identities

        :param zone: name of the zone, or domain name
        :return:
        """

        if zone is None:
            data = {}
        else:
            data = {'name': zone}

        cur_page = 1
        zone_names_to_ids = {}

        log.info('Get Cloudflare zones id\'s for zone %s' % zone)
        while True:
            zone_response = self.query_api(getattr(settings, "CLOUDFLARE_ZONE_API"), "GET", params=data, cur_page=cur_page)
            if not zone_response:
                return None

            total_pages = zone_response['result_info']['total_pages']
            for zone in zone_response['result']:
                zone_names_to_ids[zone['name']] = zone['id']
            if cur_page < total_pages:
                cur_page += 1
            else:
                break
        return zone_names_to_ids

    def get_dns_records(self, zone_id):
        """

        :param zone_id:
        :return:
        """

        dns_records = {
            'A': {},
            'AAAA': {}
        }
        dns_records_response = self.query_api(getattr(settings, 'CLOUDFLARE_ZONE_DNS_RECORDS_QUERY_API').format(zone_id=zone_id))

        for dns_record in dns_records_response['result']:
            dns_type = dns_record['type']
            name = tld.get_tld(dns_record['name'], fix_protocol=True, as_object=True)
            if dns_type == "A":
                dns_records["A"].update({name.subdomain: dns_record})
            elif dns_type == "AAAA":
                dns_records["AAAA"].update({name.subdomain: dns_record})

        return dns_records

    def update_record(self, subdomain, record_type='A', ip_address=None, ttl=1, proxied=True):
        """

        :param subdomain:
        :param record_type: DNS record type valid values: A, AAAA, CNAME, HTTPS, TXT, SRV, LOC, MX, NS, SPF, CERT,
            DNSKEY, DS, NAPTR, SMIMEA, SSHFP, SVCB, TLSA, URI read only
        :param ip_address:
        :param ttl: Time to live for DNS record. Value of 1 is 'automatic'
        :param proxied: Whether the record is receiving the performance and security benefits of Cloudflare
        :return:
        """

        record = {}

        # Extract the domain
        domain = tld.get_tld(subdomain, fix_protocol=True, as_object=True)

        # get zones ID's
        zones_ids = self.get_zones_ids(domain.fld)
        zone_dns_records = self.get_dns_records(zones_ids[domain.fld])

        if record_type == 'A':
            # check if Cloudflare has any A records
            dns_records = zone_dns_records.get('A')
            if not dns_records:
                log.error('∅ No A zone DNS records found for %s' % (domain.fld,))
                return None

            # check if the A zone dns records exist
            record = dns_records.get(domain.subdomain)
            if not record:
                log.error('∅ No DNS A record found with this name: %s' % (subdomain,))
                return None

            # because if A records will query only IPv4 IP to find out the external IP
            if not ip_address:
                if settings.QUERY_CF_FOR_EXTERNAL_IP:
                    ip_address = get_cf_ipv4()
                else:
                    ip_address = get_ipv4_address()
        elif record_type == 'AAAA':
            # check if Cloudflare has any A records
            dns_records = zone_dns_records.get('AAAA')
            if not dns_records:
                log.error('∅ No AAAA zone DNS records found for %s' % (domain.fld,))
                return None

            # check if the A zone dns records exist
            record = dns_records.get(domain.subdomain)
            if not record:
                log.error('∅ No DNS AAAA record found with this name: %s' % (subdomain,))
                return None

            # because if AAAA records will query only IPv4 IP to find out the external IP
            if not ip_address:
                ip_address = get_cf_ipv6()

        if record.get('content') == ip_address:
            log.info('⚌ DNS record is already up-to-date; taking no action')
            log.info("Date last modified: {}".format(record.get('modified_on')))
            return None

        if record and ip_address:
            log.info("📡 Updating DNS record %s" % record.get('name'))

            payload = {'type': record_type, 'name': subdomain, 'ttl': int(ttl), 'content': ip_address,
                       'proxied': bool(proxied)}

            api_endpoint = getattr(settings, 'CLOUDFLARE_ZONE_DNS_RECORDS_UPDATE_API').format(
                    zone_id=record['zone_id'], dns_record_id=record['id'])

            update_record_response = self.query_api(api_endpoint, method='PUT', json_body=payload)

            if update_record_response:
                log.info('😀 The DNS record for {} updated with new IP: {}'.format(subdomain, ip_address))
            else:
                log.error('❌ DNS record failed to update.')
        return
