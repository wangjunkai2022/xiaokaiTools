#!/usr/bin/env python3
import os
import sys
import re
import json
import base64
import argparse
import binascii
import urllib.parse

vmscheme = "vmess://"
vlessscheme = "vless://"
ssscheme = "ss://"


def parseLink(link):
    if link.startswith(ssscheme):
        return parseSs(link)
    elif link.startswith(vmscheme):
        return parseVmess(link)
    elif link.startswith(vlessscheme):
        return parseVless(link)
    else:
        print("ERROR: unsupported line: "+link)
        return None


def parseVless(link):
    if link.startswith(vlessscheme):
        linkobj = urllib.parse.urlparse(link)
        qs = urllib.parse.parse_qs(linkobj.query)
        return dict(net="vless", link=link, port=linkobj.port,
                    host=qs["host"][0], add=linkobj.hostname,
                    ps=urllib.parse.unquote(linkobj.fragment))


def parseSs(sslink):
    if sslink.startswith(ssscheme):
        ps = ""
        info = sslink[len(ssscheme):]

        if info.rfind("#") > 0:
            info, ps = info.split("#", 2)
            ps = urllib.parse.unquote(ps)

        if info.find("@") < 0:
            # old style link
            # paddings
            blen = len(info)
            if blen % 4 > 0:
                info += "=" * (4 - blen % 4)

            info = base64.b64decode(info).decode()

            atidx = info.rfind("@")
            method, password = info[:atidx].split(":", 2)
            addr, port = info[atidx+1:].split(":", 2)
        else:
            atidx = info.rfind("@")
            addr, port = info[atidx+1:].split(":", 2)

            info = info[:atidx]
            blen = len(info)
            if blen % 4 > 0:
                info += "=" * (4 - blen % 4)

            info = base64.b64decode(info).decode()
            method, password = info.split(":", 2)

        return dict(net="shadowsocks", add=addr, port=port, method=method, password=password, ps=ps)


def parseVmess(vmesslink):
    if vmesslink.startswith(vmscheme):
        bs = vmesslink[len(vmscheme):]
        # paddings
        blen = len(bs)
        if blen % 4 > 0:
            bs += "=" * (4 - blen % 4)

        vms = base64.b64decode(bs).decode()
        return json.loads(vms)
    else:
        raise Exception("vmess link invalid")


def view_loop(lines):

    def msg(x):
        if x.get("net", "") == "vless":
            return "{ps} / {net} / {add}:{port}".format(**x)
        elif x.get("net", "") == "shadowsocks":
            return "{ps} / {method} / {add}:{port}".format(**x)
        return "{ps} / {net} / {add}:{port} / net:{net}/aid:{aid}/host:{host}/path:{path}/tls:{tls}/type:{type}".format(**x)

    cnt = 0
    for _, _v in enumerate(lines):
        if _v.strip() == "":
            continue

        _vinfo = parseLink(_v)

        if _vinfo is None:
            continue

        ml = msg(_vinfo)
        cnt += 1
        print("#[{}] {}".format(cnt, ml))
        if not option.hide:
            print(_v+"\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="vmess subscribe file editor.")
    parser.add_argument('--hide', action='store_true',
                        help="hide origin vmess, just show info")
    parser.add_argument('subs',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="a subscribe text file, base64 encoded or not, or a single vmess:// ss:// link")

    option = parser.parse_args()
    indata = option.subs.read().strip()

    try:
        if indata.find("vmess") < 0:
            b64dec = indata[:]
            blen = len(b64dec)
            if blen % 4 > 0:
                b64dec += "=" * (4 - blen % 4)

            lines = base64.b64decode(b64dec).decode().splitlines()
        else:
            raise binascii.Error
    except (binascii.Error, UnicodeDecodeError):
        lines = indata.splitlines()
    finally:
        view_loop(lines)
