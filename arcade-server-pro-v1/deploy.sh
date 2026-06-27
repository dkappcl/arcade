#!/bin/bash
set -e
docker compose up -d --build
echo "Arcade PRO disponible en http://$(hostname -I | awk '{print $1}'):8990"
