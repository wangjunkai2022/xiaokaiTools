#!/bin/sh
workdir=$(cd $(dirname $0); pwd)
cd $workdir
nohup ./v2ray -config ./conf/v2ray-proxy.json >/dev/null 2>&1 &