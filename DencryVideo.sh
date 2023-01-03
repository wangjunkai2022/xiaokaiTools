#!/bin/sh
echo "解密加密视频文件"
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要解密的视频文件"
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
#outFile="${fileName%.*}"_decryption.mp4
outFile="${fileName%/*}""/decode/""${fileName##*/}"

echo "$outFile"

#文件夹是否存在 不存在就创建文件夹
if [ ! -d "${outFile%/*}" ]; then
  mkdir "${outFile%/*}"
fi

ffmpeg -decryption_key "$key" -y -i "$fileName" -c:v copy -c:a copy "$outFile"
