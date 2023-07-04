#!/bin/bash
cd ~
# run sh -c "$(curl -fsSL https://raw.githubusercontent.com/wangjunkai2022/xiaokaiTools/main/server_docker_videos.sh)"
sudo apt update
sudo apt install docker.io
sudo docker pull linuxserver/prowlarr
sudo docker pull linuxserver/sonarr
sudo docker pull linuxserver/radarr
sudo docker pull p3terx/aria2-pro
sudo docker pull emby/embyserver
sudo docker pull portainer/portainer-ce
sudo docker pull linuxserver/ombi
sudo docker pull allanpk716/chinesesubfinder
sudo docker pull linuxserver/bazarr

sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce

mkdir -p ~/videos/filse/电影
mkdir -p ~/videos/filse/电视
mkdir -p ~/videos/filse/下载

mkdir -p ~/videos/tools/prowlarr
sudo docker run -d --name=prowlarr -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC -p 9696:9696 -v ~/videos/tools/prowlarr:/config --restart always linuxserver/prowlarr:latest

mkdir -p ~/videos/tools/sonarr
sudo docker run -d --name=sonarr -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC -p 8989:8989 -v ~/videos/tools/sonarr:/config -v ~/videos/filse/电视:/tv -v ~/videos/filse/下载:/downloads --restart always linuxserver/sonarr

mkdir -p ~/videos/tools/radarr
sudo docker run -d --name=radarr -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC -p 7878:7878 -v ~/videos/tools/radarr:/config -v ~/videos/filse/电影:/movies -v ~/videos/filse/下载:/downloads --restart always linuxserver/radarr:latest

mkdir -p ~/videos/tools/aria2
sudo docker run -d --name aria2-pro --restart always --log-opt max-size=1m -e RPC_PORT=6800 -p 6800:6800 -e LISTEN_PORT=6888 -p 6888:6888 -p 6888:6888/udp -v ~/videos/tools/aria2:/config -v ~/videos/filse/下载:/downloads p3terx/aria2-pro

mkdir -p ~/videos/tools/embyserver
sudo docker run -d --name -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC embyserver -v ~/videos/tools/embyserver:/config -v ~/videos/filse/电视:/mnt/share1 -v ~/videos/filse/电影:/mnt/share2 -p 8096:8096 -p 8920:8920 --env UID=1000 --env GID=1000 --restart always emby/embyserver:latest

mkdir -p ~/videos/tools/ombi
sudo docker run -d --name=ombi -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC -e BASE_URL=/ombi -p 3579:3579 -v ~/videos/tools/ombi:/config --restart always lscr.io/linuxserver/ombi:latest


mkdir -p ~/videos/tools/chinesesubfinder/config
mkdir -p ~/videos/tools/chinesesubfinder/browser

sudo docker run -d -v ~/videos/tools/chinesesubfinder/config:/config -v ~/videos/filse/电影:/电影 -v ~/videos/filse/电视:/电视 -v ~/videos/tools/chinesesubfinder/browser:/root/.cache/rod/browser -e PUID=1026 -e PGID=100 -e PERMS=true -e TZ=Asia/Shanghai -e UMASK=022 -p 19035:19035 -p 19037:19037 --name chinesesubfinder --hostname chinesesubfinder --log-driver "json-file" --log-opt "max-size=10m" ChineseSubFinder/ChineseSubFinder

mkdir -p ~/videos/tools/bazarr
sudo docker run -d --name=bazarr -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC -p 6767:6767 -v ~/videos/tools/bazarr:/config -v ~/videos/filse/电影:/movies -v ~/videos/filse/电视:/tv --restart always lscr.io/linuxserver/bazarr:latest



