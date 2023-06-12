#!/bin/sh
# 重启V2ray
echo "重启 V2ray:     $(date)" >>/var/log/v2ray/v2ray-status.log
case "$(pidof v2ray | wc -w)" in
0)
  echo "没有启动 V2ray:     $(date)" >>/var/log/v2ray/v2ray-status.log
  ;;
1) # all ok
  echo "v2ray 正在运行 现在关闭 V2ray:  $(date)" >>/var/log/v2ray/v2ray-status.log
  kill $(pidof v2ray | awk '{print $1}')
  ;;
*)
  echo "******* Removed double V2ray: $(date)" >>/var/log/v2ray/v2ray-status.log
  kill $(pidof v2ray | awk '{print $1}')
  ;;
esac
exec ./v2ray-check-run.sh
