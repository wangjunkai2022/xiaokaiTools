#!/usr/bin/python3
import datetime
import os
import requests
from bs4 import BeautifulSoup
import re
import httpx
import asyncio

import requests
import json
from concurrent.futures import ProcessPoolExecutor

pattern = r"\?page=[a-z0-9]+"


def get_proxy_list():
    now_time = datetime.datetime.now()
    # 格式化时间字符串
    str_time = now_time.strftime("%Y-%m-%d")
    domain = "checkerproxy.net"
    url = f"https://{domain}/api/archive/{str_time}"
    # print(url)
    ips = []
    req = requests.get(url)
    if req and req.status_code == 200:
        data = json.loads(req.text)
        for ip_data in data:
            if ip_data['addr']:
                ips.append(ip_data['addr'])
    return ips


def check_proxy(proxy):
    try:
        response = requests.get('https://inapp.mypikpak.com/ping', proxies={'https': proxy}, timeout=1)
        if response.status_code == 200:
            print(f'{proxy} is working')
            return proxy
    except:
        print(f'{proxy} is not working')
        pass
    return None


def main():
    ips = get_proxy_list()
    proxies = []
    ips = ips[0:10]
    with ProcessPoolExecutor(max_workers=10) as pe:
        future_tasks = []
        for ip in ips:
            future_tasks.append(pe.submit(check_proxy(ip)))
        for future in future_tasks:
            try:
                result = future.result()
                if result:
                    proxies.append(result)
            except:
                pass

    # for proxy in ips:
    #     if check_proxy(proxy):
    #         print(proxy)
    #         proxies.append(proxy)
    #     else:
    #         print(f"{proxy} 无法ping")
    # print(proxies)
    temp_file = "ip_isOk.txt"

    # 获取当前时间
    now_time = datetime.datetime.now()
    # 格式化时间字符串
    str_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    # if not os.path.exists(temp_file):
    #     os.system(r"touch {}".format(temp_file))  # 调用系统命令行来创建文件
    input_str = f"\n\n时间:\n\t{str_time}\n{proxies}"
    with open(temp_file, 'a') as f:  # 设置文件对象
        f.write(input_str)  # 将字符串写入文件中


def ipTest():
    f = open("ips.txt")
    ips = f.read()
    ips = ips.split("\n")
    proxies = []
    for proxy in ips:
        if check_proxy(proxy):
            print(proxy)
            proxies.append(proxy)
    print(proxies)
    temp_file = "ip_isOk.txt"

    import datetime
    # 获取当前时间
    now_time = datetime.datetime.now()
    # 格式化时间字符串
    str_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    # if not os.path.exists(temp_file):
    #     os.system(r"touch {}".format(temp_file))  # 调用系统命令行来创建文件
    input_str = f"\n\n时间:\n\t{str_time}\n{proxies}"
    with open(temp_file, 'a') as f:  # 设置文件对象
        f.write(input_str)  # 将字符串写入文件中


if __name__ == '__main__':
    main()
    # ipTest()
