#!/usr/bin/env python2

import sys
import requests
from bs4 import BeautifulSoup

LIST_URL = 'https://www.eduskunta.fi/FI/kansanedustajat/Sivut/Kansanedustajat-aakkosjarjestyksessa.aspx'


def main():
    try:
        r = requests.get(LIST_URL)
        r.raise_for_status()
    except requests.HTTPError:
        print 'Could not GET listing page'
        return 1

    s = BeautifulSoup(r.content, 'lxml')
    page_urls = s.find_all('div', 'link-item')
    for page in page_urls:
        path = page.find('a').get('href')
        try:
            r = requests.get(path)
            r.raise_for_status()
        except requests.HTTPError:
            print 'Could not GET page', path
            continue
        s = BeautifulSoup(r.content, 'lxml')
        try:
            email = s.find(lambda tag: tag.get('href', '').startswith('mailto')).text
        except AttributeError:
            sys.stderr.write('No email found in %s\n' % path)
        else:
            print email

    return 0


if __name__ == '__main__':
    sys.exit(main())
