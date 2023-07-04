#!/bin/bash
cd ~
sudo apt update
sudo apt install docker.io
docker pull linuxserver/prowlarr
docker pull linuxserver/sonarr
docker pull linuxserver/radarr
docker pull p3terx/aria2-pro
docker pull emby/embyserver
docker pull portainer/portainer-ce
docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce

mkdir -p videos/filse/电影
mkdir -p videos/filse/电视
mkdir -p videos/filse/下载

mkdir -p videos/tools/prowlarr
docker run -d \
  --name=prowlarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 9696:9696 \
  -v videos/tools/prowlarr:/config \
  --restart always \
  linuxserver/prowlarr:latest

mkdir -p videos/tools/sonarr
docker run -d \
  --name=sonarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 8989:8989 \
  -v videos/tools/sonarr:/config \
  -v videos/filse/电视:/tv \
  -v videos/filse/下载:/downloads \
  --restart always \
  linuxserver/sonarr

mkdir -p videos/tools/radarr
docker run -d \
  --name=radarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 7878:7878 \
  -v videos/tools/radarr:/config \
  -v videos/filse/电影:/movies \
  -v videos/filse/下载:/downloads \
  --restart always \
  linuxserver/radarr:latest

mkdir -p videos/tools/aria2
docker run -d \
  --name aria2-pro \
  --restart always \
  --log-opt max-size=1m \
  -e RPC_PORT=6800 \
  -p 6800:6800 \
  -e LISTEN_PORT=6888 \
  -p 6888:6888 \
  -p 6888:6888/udp \
  -v videos/tools/aria2:/config \
  -v videos/filse/下载:/downloads \
  p3terx/aria2-pro

mkdir -p videos/tools/embyserver
docker run -d \
  --name embyserver \
  -v videos/tools/embyserver:/config \
  -v videos/filse/电视:/mnt/share1 \
  -v videos/filse/电影:/mnt/share2 \
  -p 8096:8096 \
  -p 8920:8920 \
  --env UID=1000 \
  --env GID=1000 \
  --restart always \
  emby/embyserver:latest
