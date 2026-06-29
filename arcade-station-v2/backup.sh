#!/bin/bash
set -e
TS=$(date +%Y%m%d_%H%M%S)
mkdir -p backup
tar -czf "backup/arcade_station_v2_${TS}.tar.gz" roms saves covers videos metadata .env docker-compose.yml
echo "Backup creado: backup/arcade_station_v2_${TS}.tar.gz"
