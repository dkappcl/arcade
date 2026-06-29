#!/bin/bash
set -e

echo "== Arcade Station v2 =="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado. Instalando Docker para CentOS 9..."
  sudo dnf -y install dnf-plugins-core
  sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl enable --now docker
fi

mkdir -p roms/{arcade,nes,snes,sega,neogeo,atari,gb,gba,gbc}
mkdir -p covers/{arcade,nes,snes,sega,neogeo,atari,gb,gba,gbc}
mkdir -p saves videos metadata backup

docker compose config >/dev/null
docker compose up -d --build

echo ""
docker compose ps
echo ""
echo "Disponible en: http://$(hostname -I | awk '{print $1}'):8990"
