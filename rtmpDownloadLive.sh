url="rtmp://pull0csp7bqtxeaj.ntjpnz.com/live/1604172653_532f3047d07fc7eca137c1b86c59d540?token=727705fccf9c4cf7a73aa1786106da90&t=1675655185"
name=$(echo $url | grep -Eo "live/[0-9]+")
name=${name:5}
echo $name