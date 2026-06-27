#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-/u01/arcade-docker}"
PORT="8990"

echo "==> Instalando dependencias base"
sudo dnf -y install dnf-plugins-core git curl firewalld || true

if ! command -v docker >/dev/null 2>&1; then
  echo "==> Instalando Docker CE"
  sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

sudo systemctl enable --now docker
sudo systemctl enable --now firewalld || true
sudo firewall-cmd --permanent --add-port=${PORT}/tcp || true
sudo firewall-cmd --reload || true

sudo mkdir -p "$APP_DIR"
sudo chown -R "$USER:$USER" "$APP_DIR"

echo "==> Copia este proyecto en: $APP_DIR"
echo "==> Luego ejecuta: docker compose up -d --build"
echo "==> URL: http://IP_DEL_SERVIDOR:${PORT}"
