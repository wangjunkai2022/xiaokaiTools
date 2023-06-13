#!/bin/sh
# 使用私密的gitee

owner="kaikai2024"                              #仓库所属空间地址(企业、组织或个人的地址path)
repo="test"                                     #仓库路径(path)
path="config.json"                              #文件的路径
access_token="083da81825587ba20ee88b6424954b89" #用户授权码
cd $(dirname $0)

function get_json_value() {
  local json=$1
  local key=$2

  if [[ -z "$3" ]]; then
    local num=1
  else
    local num=$3
  fi

  local value=$(echo "${json}" | awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'${key}'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${num}p)

  echo ${value}
}

path_url="https://gitee.com/api/v5/repos/$owner/$repo/contents/$path?access_token=$access_token"
curl_data=$(curl -X GET --header 'Content-Type: application/json;charset=UTF-8' $path_url)
#echo $curl_data
content=$(get_json_value $curl_data "content")
echo $(base64 -d <<<$content) >temp # 解密Base64并把文件内容写到temp文件中
