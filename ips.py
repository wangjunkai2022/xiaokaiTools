import requests
from bs4 import BeautifulSoup
import re

pattern = r"\?page=[a-z0-9]+"


def get_proxy_list(url):
    print(url)
    proxies = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        ip = columns[0].text.strip()
        port = columns[1].text.strip()
        proxy = f'{ip}:{port}'
        proxies.append(proxy)
        if check_proxy(proxy):
            print(proxy)
            return
    if re.search(pattern, url):
        url = re.sub(pattern, pageNext(soup), url)
    else:
        url = url + pageNext(soup)
    get_proxy_list(url)


import requests


def check_proxy(proxy):
    try:
        response = requests.get('https://inapp.mypikpak.com/ping', proxies={'https': proxy}, timeout=2)
        if response.status_code == 200:
            print(f'{proxy} is working')
            return True
    except:
        print(f'{proxy} is not working')

    return False


def pageNext(content):
    link = content.prettify()
    pattern_next = r'<a aria-label="Next" href="(\?page=\w+)">'
    match = re.findall(pattern_next, link)

    if match:
        # page_param = match.group()
        print(match[0])
        return match[0]
    else:
        print("No match found")


def main():
    url = 'https://ip.ihuan.me/'  # 替换为目标网站的URL
    get_proxy_list(url)


if __name__ == '__main__':
    main()
