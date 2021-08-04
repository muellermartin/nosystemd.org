#!/usr/bin/env python3

import sys

from bs4 import BeautifulSoup
from colorama import Fore, Style
import colorama
import requests


def checklink(url, headers=None):
    try:
        response = requests.head(url, allow_redirects=True, headers=headers)

        if response.status_code == 200:
            ok = True
        # 403 = forbidden
        # Some shitty WAFs seem to dislike Python as user agent
        # -> fake user agent
        elif response.status_code == 403:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
            return checklink(url, headers={'User-Agent': user_agent}) 
        # 405 = method not allowed
        # -> retry with GET
        elif response.status_code == 405:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                ok = True
            else:
                ok = False
        else:
            ok = False
    except requests.exceptions.SSLError:
        ok = False
        print('SSL error for {}'.format(url), file=sys.stderr)
    except requests.ConnectionError:
        ok = False
        print('Can\'t connect to {}'.format(url), file=sys.stderr)

    if ok:
        print(Fore.GREEN + 'OK' + Style.RESET_ALL)
        return True

    print(Fore.RED + 'FAIL' + Style.RESET_ALL)
    return False


def main():
    with open('htdocs/index.html') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    for anchor in soup.find_all('a'):
        url = anchor['href']

        if url.startswith('http'):
            print('Checking URL {}'.format(url))
            checklink(url)


if __name__ == '__main__':
    colorama.init()
    main()
