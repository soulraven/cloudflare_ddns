#!/usr/bin/env python3
#   -*- coding: utf-8 -*-
#       Copyright (C) 2018-2021 ProGeek
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
import sys
import time
import logging
import threading

import schedule

from cloudflare_ddns.conf import settings
from cloudflare_ddns.utils.log import configure_logging
# from libs.utils import load_arguments, load_conf
# from libs.logging.logging import configure_logging

from cloudflare_ddns.Cloudflare import Cloudflare

log = logging.getLogger('cf_logging')
schedule_logger = logging.getLogger('schedule')


def cloudflare_job(**kwargs):
    """

    :param kwargs:
    :return:
    """
    cf = Cloudflare()
    cf(subdomain=kwargs['dns_record'], record_type=kwargs['record_type'], ttl=kwargs['ttl'], proxied=kwargs['proxied'])


def cloudflare_generator():
    while True:
        for x in settings.CF_SUBDOMAINS:
            if x.get('state'):
                run_threaded(cloudflare_job, **x)
                yield


generator_job = cloudflare_generator()


def run_threaded(job_func, **kwargs):
    job_thread = threading.Thread(target=job_func, kwargs=kwargs)
    job_thread.daemon = True
    job_thread.name = kwargs['dns_record']
    job_thread.start()
    job_thread.join()


if __name__ == '__main__':
    log.info("Start the Cloudflare DDNS script")

    schedule.every(settings.SCHEDULE_DELAY_TASKS).seconds.do(lambda: next(generator_job))

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        schedule.clear()
        log.warning("Cloudflare DDNS script interrupted")
        sys.exit(1)
