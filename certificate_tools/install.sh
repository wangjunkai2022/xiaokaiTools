#!/bin/bash

# 检查是否提供了 PEM 文件作为参数
if [ "$#" -ne 1 ]; then
    echo "用法: $0 <pem_file>"
    exit 1
fi

# 获取 PEM 文件
PEM_FILE=$1

# 检查文件是否存在
if [ ! -f "$PEM_FILE" ]; then
    echo "文件 $PEM_FILE 不存在."
    exit 1
fi

# 计算哈希值
HASH_VALUE=$(openssl x509 -subject_hash_old -in "$PEM_FILE" | sed -n '1p')

# 复制文件并重命名
cp "$PEM_FILE" "${HASH_VALUE}.0"

echo "文件已复制为 ${HASH_VALUE}.0"

HASH_FILE=${HASH_VALUE}.0

# 获取当前连接的设备列表
DEVICES=$(adb devices | grep -w "device" | awk '{print $1}')

# 计算设备数量
DEVICE_COUNT=$(echo "$DEVICES" | wc -l)

# 如果没有设备连接
if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "没有连接的设备."
    exit 1
fi

# 如果只有一个设备，直接使用该设备
if [ "$DEVICE_COUNT" -eq 1 ]; then
    SELECTED_DEVICE=$(echo "$DEVICES" | head -n 1)
else
    # 如果有多个设备，列出设备供用户选择
    echo "请从以下设备中选择一个:"
    PS3="选择设备: "
    select SELECTED_DEVICE in $DEVICES; do
        if [[ -n "$SELECTED_DEVICE" ]]; then
            break
        else
            echo "无效选择，请重试."
        fi
    done
fi

# 先获取root
adb -s "$SELECTED_DEVICE" root
# 获取访问权限
adb -s "$SELECTED_DEVICE" remount

# 将 证书 文件推送到设备
adb -s "$SELECTED_DEVICE" push ${HASH_FILE} /system/etc/security/cacerts/

# 进入设备 shell 并执行命令
adb -s "$SELECTED_DEVICE" shell <<EOF
chmod -R 755 /system/etc/security/cacerts/${HASH_FILE}
EOF
adb -s "$SELECTED_DEVICE" reboot

echo "安装${PEM_FILE}到设备成功"