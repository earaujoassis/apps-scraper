#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urlparse
import ssl
import re
import os
import json
import sys
from bs4 import BeautifulSoup


def scrap_data(apps):
    scrapped_data = []
    for app_name, app_public_url in apps.items():
        try:
            public_page = urllib2.urlopen(app_public_url, timeout=5)
        except ssl.SSLError as e:
            sys.stderr.write('Connection timed out; please check your internet connection\n')
            continue
        except urllib2.URLError as e:
            sys.stderr.write('Connectivity issue; please check your internet connection; exiting\n')
            sys.exit(-1)

        if public_page.getcode() != 200:
            continue
        soup = BeautifulSoup(public_page, 'html.parser')
        name = soup.find('h1', attrs={'class': 'product-header__title'}).contents[0].strip()
        languages = soup.find('dt',
                              attrs={'class': 'information-list__item__term'},
                              string=re.compile('Languages')).next_sibling.next_sibling.text.strip().split(',')
        languages = sorted([language.strip() for language in languages])
        minimum_system_version_box = soup.find('dt',
                                               attrs={'class': 'information-list__item__term'},
                                               string=re.compile('Compatibility')).next_sibling.next_sibling.text.strip()
        minimum_system_version_regex_groups = re.search('((\d+\.)?(\d+\.)?(\*|\d+))', minimum_system_version_box)
        minimum_system_version = minimum_system_version_regex_groups.group(1) if minimum_system_version_regex_groups else None
        app_identifier = int(urlparse.urlparse(app_public_url).path.split('/')[-1].replace('id', ''))
        scrapped_data.append({
            'languages': languages,
            'app_identifier': app_identifier,
            'name': name,
            'minimum_ios_version': minimum_system_version,
        })
    return scrapped_data


def generate_apps_json(scrapped_data, filename='apps.json'):
    _remove_filename(filename)
    with open(filename, 'w') as outfile:
        json.dump(scrapped_data, outfile, indent=4, separators=(',', ': '))


def generate_filtered_apps_json(scrapped_data, filename='filtered_apps.json'):
    _remove_filename(filename)
    filtered_data = {
        'apps_in_spanish_and_tagalog': \
            sorted(map(
                lambda x: x['app_identifier'],
                filter(
                       lambda x: 'Spanish' in x['languages'] and 'Tagalog' in x['languages'],
                       scrapped_data))),
        'apps_with_insta_in_name': \
            sorted(map(
                lambda x: x['app_identifier'],
                filter(
                       lambda x: 'INSTA' in x['name'].upper(),
                       scrapped_data)))
    }
    with open(filename, 'w') as outfile:
        json.dump(filtered_data, outfile, indent=4, separators=(',', ': '))


def _remove_filename(filename):
    if os.path.isfile(filename):
        os.remove(filename)
