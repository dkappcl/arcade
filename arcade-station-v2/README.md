# Arcade Station v2

Consola arcade web en Docker para CentOS 9.

## Incluye

- Web en puerto 8990
- Backend FastAPI
- Nginx
- Catálogo automático
- Subida de ROMs legales desde navegador
- Subida de carátulas
- Botón Jugar
- Player web preparado con EmulatorJS vía CDN
- Scripts deploy y backup

## Importante

No incluye ROMs, BIOS ni juegos comerciales.

## Instalación

```bash
cd /u01/arcade
unzip arcade-station-v2.zip
cd arcade-station-v2
chmod +x deploy.sh backup.sh
./deploy.sh
```

Abrir:

```text
http://IP_SERVIDOR:8990
```

## Comandos útiles

```bash
docker compose ps
docker compose logs -f
docker compose restart
docker compose down
```

## Agregar ROMs

Desde la web usa "Subir ROM legal" o por consola:

```bash
cp juego.zip roms/arcade/
cp juego.nes roms/nes/
cp juego.sfc roms/snes/
```

## Modo offline

Esta versión carga EmulatorJS desde CDN. Para dejarlo offline, copia EmulatorJS local en:

```text
frontend/emulatorjs/
```

y ajusta `frontend/player.js`.
