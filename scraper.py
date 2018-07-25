#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import scraper


def process_input_file(filename):
    apps = {}
    if os.path.isfile(filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['App Store URL'].startswith('https://itunes.apple.com/us/app/'):
                    apps[row['App Name']] = row['App Store URL']
    return apps


def main():
    if len(sys.argv) < 2:
        sys.stderr.write('Missing input file path; exiting\n')
        sys.exit(-1)
    try:
        data = scraper.scrap_data(process_input_file(sys.argv[1]))
    except Exception as e:
        sys.stderr.write('Connectivity issue; please check your internet connection; exiting\n')
        sys.exit(-1)

    scraper.generate_apps_json(data)
    scraper.generate_filtered_apps_json(data)


if __name__ == '__main__':
    main()
