#!/bin/sh
echo "ffmpeg视频文件转M3U8"
if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要转换的视频文件"
  # shellcheck disable=SC2162
  read input
else
  input=$1
fi
echo "input"

#文件路径
filePath="${input%/*}"
#文件全名
fileNameAll="${input##*/}"
#文件后缀
fileSuffix="${input##*.}"
#文件名不含后缀
fileName="${fileNameAll%.*}"

#在原来的视频路径下拼接一个新的文件夹以文件名字命名
outFile="$filePath/$fileName"
echo "$outFile"

#文件夹是否存在 不存在就创建文件夹
if [ ! -d "$outFile" ]; then
  mkdir "$outFile"
fi

#工作路径切换到需要存的视频路径下
cd $outFile
ffmpeg -i $input -y -vcodec copy -acodec copy -hls_enc 1 -hls_enc_key aaaaaaaaaaaaaaaa -hls_segment_filename 'file_data_%04d.ts' -hls_playlist_type vod -hls_time 6 -hls_list_size 0 $fileName.m3u8

