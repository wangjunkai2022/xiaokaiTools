#!/bin/sh
echo "开启 Docker 下载完成后回自动关闭"

if [ -z "$1" ]; then
  # shellcheck disable=SC2028
  echo "请输入需要地址\n"
  # shellcheck disable=SC2162
  read url
else
  url=$1
  echo "$url"
fi

# shellcheck disable=SC2028
echo "输入序号执行操作\n1:下载高清视频 \n2:下载MP3声音 \n其他:手动下载"
# shellcheck disable=SC2162
read opation

if [ "$opation" -eq "1" ]; then
  echo "下载最高质量"
  # echo "正在下载：$1"
  docker run -it --rm -v /Users/evan/Downloads/ytdlp:/media tnk4on/yt-dlp -f "ba+bv" "$url" --merge-output-format mp4
elif [ "$opation" -eq "2" ]; then
  echo "下载最高质量声音并转换MP3"
  docker run -it --rm -v /Users/evan/Downloads/ytdlp:/media tnk4on/yt-dlp -f 'ba' -x --audio-format mp3 "$url"
#elif [ "$opation" -eq "3" ]; then
##  echo "ffplay播放最高质量视频"
#  docker run -it --rm -v /Users/evan/Downloads/ytdlp:/media -v tnk4on/yt-dlp  $url -o - | ffplay -
else
  echo "获取可以下载列表中..."
  docker run -it --rm -v /Users/evan/Downloads/ytdlp:/media tnk4on/yt-dlp -F "$url"
  # shellcheck disable=SC2028
  echo "输入选中的列表id \n"
  # shellcheck disable=SC2162
  read number
  docker run -it --rm -v /Users/evan/Downloads/ytdlp:/media tnk4on/yt-dlp -f $number "$url"
fi
