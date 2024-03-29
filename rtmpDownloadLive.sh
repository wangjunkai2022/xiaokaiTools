#!/bin/sh
echo "下载rtmp直播为mp4"

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

time=$(date "+%Y%m%d-%H%M%S")
name=$(echo $url | grep -Eo "live/[0-9]+")
name=${name:5}-$time.mp4
echo $name

ffmpeg -i "$url live=1 timeout=1" -t 03:00:00 -vcodec copy -acodec copy -f mp4 $name
