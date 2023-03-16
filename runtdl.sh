#!/bin/sh
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入TG 消息地址\n"
  # shellcheck disable=SC2162
  read url
else
  url=$1
  echo "$url"
fi

if [ -z "$2" ]; then
  downloadDir=~/Downloads/TDL/
else
  downloadDir=$2
  echo "存档路径为:$downloadDir"
fi

#文件夹是否存在 不存在就创建文件夹
if [ ! -d "$downloadDir" ]; then
  mkdir "$downloadDir"
fi
docker run -it --rm -v $downloadDir:/downloads/ tdlrun "$url"
