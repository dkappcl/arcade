#!/bin/bash
set -e

echo "== Arcade Station v1 =="
echo "Verificando Docker..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado. Instalando dependencias base para CentOS 9..."
  sudo dnf -y install dnf-plugins-core
  sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl enable --now docker
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Falta Docker Compose plugin."
  exit 1
fi

mkdir -p roms/arcade roms/nes roms/snes roms/sega roms/neogeo roms/atari saves covers videos metadata backup

echo "Levantando servicios..."
docker compose up -d --build

echo ""
echo "Arcade Station disponible en:"
echo "http://$(hostname -I | awk '{print $1}'):8990"
echo ""
echo "Para ver logs:"
echo "docker compose logs -f"
