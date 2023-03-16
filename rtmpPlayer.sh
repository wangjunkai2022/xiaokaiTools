#!/bin/sh
echo "播放rtmp直播"
#url="rtmp://pull0csp7bqtxeaj.ntjpnz.com/live/1604172653_532f3047d07fc7eca137c1b86c59d540?token=727705fccf9c4cf7a73aa1786106da90&t=1675655185"
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要地址\n"
  # shellcheck disable=SC2162
  read url
else
  url=$1
  echo "$url"
fi

ffplay -i "$url live=1 timeout=1"

#rtmp://pull7kv5kqq7k77g.nmhcxx.com/live/804322423_cdc3d60973ca0f8b0e757edfd9b34240?token=43f3f62fbd2083d03eca433370f77fa7&t=1675760838