#!/bin/bash
set -e
echo "== Arcade Station v2 EmulatorJS =="
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado. Instalando Docker para CentOS 9..."
  sudo dnf -y install dnf-plugins-core
  sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl enable --now docker
fi
mkdir -p roms/arcade roms/nes roms/snes roms/sega roms/neogeo roms/atari roms/gba roms/gb roms/gbc saves covers videos metadata backup
docker compose down || true
docker compose up -d --build
echo ""
echo "Arcade Station disponible en:"
echo "http://$(hostname -I | awk '{print $1}'):8990"
