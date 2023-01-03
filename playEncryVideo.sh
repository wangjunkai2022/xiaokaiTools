#!/bin/sh
echo "播放加密视频文件"
#设置播放的速度 1是正常播放速度
play_speed=1
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要播放的视频文件"
  # shellcheck disable=SC2162
  read fileName
else
  fileName=$1
fi
echo "$fileName"

if [ -z "$2" ]; then
  key=$(cat ./key.txt)
else
  key=$2
fi
echo "$key"
ffplay -i "$fileName" -decryption_key "$key" -vf setpts=PTS/$play_speed -af atempo=$play_speed
