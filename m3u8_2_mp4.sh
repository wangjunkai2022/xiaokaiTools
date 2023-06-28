#!/bin/bash

# 获取传入的路径
input_path=$1

if [ -d $input_path ]; then
  #  file_name=$(basename $input_path)
  #  parent_name=$(dirname $input_path)
  #  获取文件夹下所有文件
  files=$(ls $input_path)
  # 遍历文件列表，找出名字是m3u8后缀的文件
  for file in $files; do
    if [[ $file == *.m3u8 ]]; then
      input_path="$input_path/$file"
    fi
  done
fi
if [[ $input_path == *.m3u8 ]]; then
  #  获取没有后缀的文件名
  file_name=$(basename $input_path)
  file_name="${file_name%.*}"
  # 获取m3u8文件所在文件夹的父文件夹
  parent_name=$(dirname $(dirname $input_path))
#  echo $file_name
#  echo $parent_name
else
  echo "文件不是m3u8的视频文件"
  exit 200
fi
cd $parent_name

ffmpeg -allowed_extensions ALL -i "$input_path" -c copy "$file_name.mp4"
echo "转换完成的文件是 $parent_name/$file_name.mp4"
