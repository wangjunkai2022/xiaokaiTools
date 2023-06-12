#!/bin/sh
REMOTE_ADDR="https://raw.githubusercontent.com/wangjunkai2022/v2config/main"
CONFIG_FILE="bridge.json"
LOCAL_FILE="bridge.json"
mkdir /var/log/v2ray/
# 从远端下载config文件，保存为temp文件
curl -o temp "${REMOTE_ADDR}/${CONFIG_FILE}"

# 比较temp和本地文件是否相同
if cmp -s "${LOCAL_FILE}" temp; then
  echo "本地文件和远端config文件相同 :$(date)" >>/var/log/v2ray/v2ray-status.log
  rm -rf temp
  exec ./v2ray-check-run.sh
else
  echo "本地文件和远端config文件不同，替换本地文件 :$(date)" >>/var/log/v2ray/v2ray-status.log
  mv temp "${LOCAL_FILE}"
  cp $LOCAL_FILE config.json
  exec ./v2ray-restart.sh
fi
