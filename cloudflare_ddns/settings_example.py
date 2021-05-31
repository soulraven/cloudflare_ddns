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

DEBUG = False

# Cloudflare account domains that will update DNS records
CF_SUBDOMAINS = [
    {
        'dns_record': 'subdomain-1.domain.tld',
        'record_type': 'AAAA',
        'ttl': 1,
        'proxied': False,
        'state': True
    },
    {
        'dns_record': 'subdomain-2.domain.tld',
        'record_type': 'A',
        'ttl': 1,
        'proxied': False,
        'state': True
    }
]

# Cloudflare API authentication type. Permitted token or key
CF_AUTH_TYPE = 'token'

# Cloudflare API Token used for cf_auth_type == token
CF_API_TOKEN = '<some api token>'

# Cloudflare used for cf_auth_type == key
CF_API_KEY = '<some api key>'

# Cloudflare email account
CF_EMAIL = '<some email account for cloudflare>'

# Time to live for DNS record. Value of 1 is 'automatic'
CF_DEFAULT_TTL = 300

# Whether the record is receiving the performance and security benefits of Cloudflare
CF_PROXIED = True

###########################
# Cloudflare zone API URL #
###########################
# The stable base URL for all Version 4 HTTPS endpoints
CLOUDFLARE_ENDPOINT_API = 'https://api.cloudflare.com/client/v4'  # GET
CLOUDFLARE_USER_API = 'https://api.cloudflare.com/client/v4/user'  # GET
CLOUDFLARE_ZONE_API = 'https://api.cloudflare.com/client/v4/zones'  # GET
CLOUDFLARE_ZONE_DNS_RECORDS_QUERY_API = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'  # GET
CLOUDFLARE_ZONE_DNS_RECORDS_UPDATE_API = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{' \
                                         'dns_record_id}'  # PATCH

#############################
# External IP query API's #
#############################

QUERY_CF_FOR_EXTERNAL_IP = True

# Cloudflare api service that returns IPv6 IP
EXTERNAL_CF_IPV6_QUERY_API = 'https://[2606:4700:4700::1111]/cdn-cgi/trace'

# Cloudflare api service that returns IPv4 IP
EXTERNAL_CF_IPV4_QUERY_API = 'https://1.1.1.1/cdn-cgi/trace'

# all api services returns only IPv4 IP
EXTERNAL_IPV4_QUERY_APIS = [
    'https://api.ipify.org',
    'https://checkip.amazonaws.com',
    'https://v4.ident.me/',
    'https://ifconfig.me/ip',
    'https://ipv4.icanhazip.com/',
    'https://api.simonpainter.com/ip/'
]

#############################
# Global settings           #
#############################

# how many seconds each task will be delayed from the next task
SCHEDULE_DELAY_TASKS = 30 * 60

###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}
