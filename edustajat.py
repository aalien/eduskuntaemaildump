#!/usr/bin/env python3.7

import sys
import requests
from bs4 import BeautifulSoup

LIST_URL = 'https://www.eduskunta.fi/FI/kansanedustajat/Sivut/Kansanedustajat-aakkosjarjestyksessa.aspx'


def main():
    try:
        r = requests.get(LIST_URL)
        r.raise_for_status()
    except requests.HTTPError:
        sys.stderr.write('Could not GET listing page\n')
        return 1

    s = BeautifulSoup(r.content, 'html.parser')
    page_urls = s.find_all('div', 'link-item')
    for page in page_urls:
        path = page.find('a').get('href')
        try:
            r = requests.get(path)
            r.raise_for_status()
        except requests.HTTPError:
            sys.stderr.write(f'Could not GET page {path}\n')
            continue
        s = BeautifulSoup(r.content, 'html.parser')
        try:
            email = s.find('div', id='ctl00_PlaceHolderMain_MOPInformation_EmailPanel').find('div', class_='mop-info-value').text.strip().replace('(at)', '@')
        except AttributeError:
            sys.stderr.write(f'No email found in {path}\n')
        else:
            print(email)
            sys.stdout.flush()

    return 0


if __name__ == '__main__':
    sys.exit(main())
