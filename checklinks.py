#!/usr/bin/env python3

import sys

from bs4 import BeautifulSoup
from colorama import Fore, Style
import colorama
import requests


def main():
    with open('htdocs/index.html') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    for anchor in soup.find_all('a'):
        url = anchor['href']

        if url.startswith('http'):
            print('Checking URL {}'.format(url))

            try:
                response = requests.head(url, allow_redirects=True)

                if response.status_code == 200:
                    ok = True
                # 405 = method not allowed -> retry with GET
                elif response.status_code == 405:
                    response = requests.get(url)

                    if response.status_code == 200:
                        ok = True
                    else:
                        ok = False
                else:
                    ok = False
            except requests.ConnectionError:
                ok = False
                print('Can\'t connect to {}'.format(url), file=sys.stderr)

            if ok:
                print(Fore.GREEN + 'OK' + Style.RESET_ALL)
            else:
                print(Fore.RED + 'FAIL' + Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    main()
