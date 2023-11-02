#!/bin/sh
rm -rf temp
downsh="gitee-download.sh"
source ./$downsh
# 配置文件检查
source ./v2ray-config-check.sh

if [ -f temp ]; then
  if cmp -s "${LOCAL_FILE}" temp; then
    echo "本地文件和远端config文件相同 :$(date)" #>>/var/log/v2ray/v2ray-status.log
    rm -rf temp
    exec ./v2ray-check-run.sh
  else
    echo "本地文件和远端config文件不同，替换本地文件 :$(date)" #>>/var/log/v2ray/v2ray-status.log
    mv temp "${LOCAL_FILE}"
    cp $LOCAL_FILE config.json
    exec ./v2ray-restart.sh
  fi
else
  echo "本地文件temp不存在直接检测 :$(date)" #>>/var/log/v2ray/v2ray-status.log
  exec ./v2ray-check-run.sh
fi
