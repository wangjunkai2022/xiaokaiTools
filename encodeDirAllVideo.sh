#!/bin/sh
echo "加密文件夹下所有的视频文件"
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要加密的视频文件夹"
  # shellcheck disable=SC2162
  read dir
else
  dir=$1
#  echo "$dir"
fi

python3 runAllFile.py -c ./encode.sh -d "$dir" -s .mov.mp4.m4a.3gp.3g2.flv
