#!/usr/bin/env python2

import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.eduskunta.fi'
LIST_PATH = '/triphome/bin/hex3000.sh'


def main():
    try:
        r = requests.get(''.join((BASE_URL, LIST_PATH)))
        r.raise_for_status()
    except requests.HTTPError:
        print 'Could not GET listing page'
        return 1

    s = BeautifulSoup(r.content)
    page_urls = s.find('div', 'listing').find_all('a')
    for page in page_urls:
        path = page.get('href')
        try:
            r = requests.get(''.join((BASE_URL, path)))
            r.raise_for_status()
        except requests.HTTPError:
            print 'Could not GET page', path
            continue
        s = BeautifulSoup(r.content)
        try:
            email = s.find('span', 'emailAddress').text.replace('[at]', '@')
        except AttributeError:
            sys.stderr.write('No email found: %s\n' % s)
        else:
            print email

    return 0


if __name__ == '__main__':
    sys.exit(main())
