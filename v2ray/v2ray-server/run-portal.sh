#!/bin/sh
workdir=$(cd $(dirname $0); pwd)
cd $workdir
nohup ./v2ray -config ./conf/portal.json >/dev/null 2>&1 &