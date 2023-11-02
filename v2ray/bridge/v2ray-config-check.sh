#!/bin/sh
FIND_FILE="temp"
FIND_STR="Configuration OK."

v2ray=~/Downloads/v2ray-macos-64/v2ray #v2ray执行路径

config_file="$(
  cd "$(dirname "$0")"
  pwd
)/$FIND_FILE"
echo $config_file
#$v2ray test "$config_file"
checkRule=$(echo $($v2ray "test" temp))
##checkRule=$(echo $v2ray "test" "$(basename $0)/$FIND_FILE)")
#echo $checkRule
### 判断匹配函数，匹配函数不为0，则包含给定字符
result=$(echo $checkRule | grep "${FIND_STR}")
if [[ "$result" != "" ]]; then
  echo "配置文件ok"
else
  echo "配置文件 无法使用"
  rm -rf config_file
fi
