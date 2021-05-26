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

DEBUG = True

# Cloudflare account domains
CF_DOMAINS = ['progeek.ro']

# Cloudflare API authentication type. Permitted token or key
CF_AUTH_TYPE = 'token'

# Cloudflare API Token used for cf_auth_type == token
CF_API_TOKEN = '<some api token>'

# Cloudflare used for cf_auth_type == key
CF_API_KEY = '<some api key>'

# Cloudflare email account
CF_EMAIL = '<some email account for cloudflare>'

CF_IPV6 = True

CF_IPV4 = True

# Cloudflare default TTL
CF_DEFAULT_TTL = 300

###########################
# Cloudflare zone API URL #
###########################

CLOUDFLARE_ZONE_QUERY_API = 'https://api.cloudflare.com/client/v4'  # GET
CLOUDFLARE_ZONE_DNS_RECORDS_QUERY_API = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'  # GET
CLOUDFLARE_ZONE_DNS_RECORDS_UPDATE_API = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'  # PATCH

#############################
# External IP query API's #
#############################

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

###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}
