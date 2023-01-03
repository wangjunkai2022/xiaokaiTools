#!/bin/sh
echo "解密文件夹下所有的视频文件"
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要解密的视频文件夹"
  # shellcheck disable=SC2162
  read dir
else
  dir=$1
#  echo "$dir"
fi

python3 runAllFile.py -c ./DencryVideo.sh -d "$dir" -s .mp4
