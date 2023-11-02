#!/bin/sh
case "$(pidof v2ray | wc -w)" in
0)  echo "Restarting V2ray:     $(date)" >> /var/log/v2ray/v2ray-status.log
    nohup /jffs/v2ray/v2ray --config=/jffs/v2ray/config.json >/dev/null 2>&1 &
    ;;
1)  # all ok
    ;;
*)  echo "Removed double V2ray: $(date)" >> /var/log/v2ray/v2ray-status.log
    kill $(pidof v2ray | awk '{print $1}')
    ;;
esac