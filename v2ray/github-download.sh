#!/bin/sh
#使用github下载
REMOTE_ADDR="https://raw.githubusercontent.com/wangjunkai2022/v2config/main"
CONFIG_FILE="bridge.json"
# 从远端下载config文件，保存为temp文件
curl -o temp "${REMOTE_ADDR}/${CONFIG_FILE}"
