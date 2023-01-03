#!/bin/sh
echo "加密视频文件"

if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要加密的视频文件"
  # shellcheck disable=SC2162
  read fileName
else
  fileName=$1
#  echo "$fileName"
fi

if [ -z "$2" ]; then
  basepath=$(
    cd $(dirname $0)
    pwd
  )
  echo "$basepath"
  key=$(cat "$basepath"/key.txt)
else
  key=$2
#  echo "$key"
fi

if [ "${fileName##*.}"x = "mp4"x ]; then
  #  echo "文件是mp4"
  tempVideo="$fileName"
  #  fileName="${fileName%.*}"_encry.mp4
  fileName="${fileName%/*}""/encode/""${fileName##*/}"
else
  #  echo "文件不是mp4"
  tempVideo="${fileName%.*}".mp4
  ffmpeg -y -i "$fileName" -vcodec copy -acodec copy "$tempVideo"
  #  ffmpeg -y -i "$fileName" "$tempVideo"
  #  echo "$tempVideo"
  isTempFile=true
  #  fileName="${fileName%.*}"_encry.mp4
  fileName="${fileName%/*}""/encode/""${fileName##*/}"".mp4"
fi
#echo "$fileName"

#文件夹是否存在 不存在就创建文件夹
if [ ! -d "${fileName%/*}" ]; then
  mkdir "${fileName%/*}"
fi

#加密命令
ffmpeg -y -i "$tempVideo" -c:v copy -c:a copy -encryption_scheme cenc-aes-ctr -encryption_key "$key" -encryption_kid aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1 "$fileName"

#加密完成 删除临时文件
if [ "$isTempFile" == "true" ]; then
  #  echo "删除临时文件""$tempVideo"
  rm "$tempVideo"
fi
