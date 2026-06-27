# Arcade Station v1

Arcade Station es una base Docker portable para administrar un catálogo arcade desde web.

## Importante sobre ROMs

Este proyecto no incluye juegos ni ROMs. Debes usar únicamente ROMs, BIOS y archivos de los que tengas derecho de uso.

## Requisitos CentOS 9

- CentOS Stream 9
- Docker y Docker Compose plugin
- Puerto 8990 disponible

## Instalación rápida

```bash
cd /u01
unzip arcade-station-v1.zip
cd arcade-station-v1
chmod +x deploy.sh backup.sh
./deploy.sh
```

Abrir:

```text
http://IP_DEL_SERVIDOR:8990
```

## Carpetas de ROMs

```text
roms/arcade
roms/neogeo
roms/nes
roms/snes
roms/sega
roms/atari
```

## Comandos útiles

```bash
docker compose ps
docker compose logs -f
docker compose restart
docker compose down
```

## Backup

```bash
./backup.sh
```

## Cloudflare Tunnel

Puedes publicar con una ruta hacia:

```text
http://localhost:8990
```

Ejemplo de dominio:

```text
arcade.dkapp.cl
```

## Próxima versión sugerida

- Integración EmulatorJS para jugar desde navegador.
- Descarga automática de carátulas locales.
- Login administrador.
- Favoritos persistentes.
- Estadísticas de uso.
- Configuración de controles.
