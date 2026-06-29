# Arcade Station v2 con EmulatorJS

Versión con catálogo, subida de ROMs legales y botón **Jugar** desde navegador.

## Importante

Este proyecto no incluye juegos, ROMs ni BIOS. Usa únicamente archivos sobre los que tengas derecho de uso.

## Levantar en CentOS 9

```bash
cd /u01/arcade
unzip arcade-station-v2-emulatorjs.zip
cd arcade-station-v2-emulatorjs
chmod +x deploy.sh backup.sh
./deploy.sh
```

Abrir:

```text
http://IP_SERVIDOR:8990
```

## Migrar ROMs desde v1

```bash
cd /u01/arcade
cp -a arcade-station-v1/roms/* arcade-station-v2-emulatorjs/roms/
cd arcade-station-v2-emulatorjs
./deploy.sh
```

## Uso

1. Abre la web.
2. Selecciona el sistema.
3. Sube una ROM legal.
4. Presiona **Jugar**.

## Recomendado para probar primero

- NES: `.nes`
- SNES: `.sfc`, `.smc`
- Sega: `.gen`, `.md`
- Game Boy: `.gb`, `.gbc`
- Game Boy Advance: `.gba`
- Atari: `.a26`

## MAME / Neo Geo

MAME y Neo Geo pueden requerir ZIP correcto, versión de romset compatible y BIOS.

## Comandos

```bash
docker compose ps
docker compose logs -f
docker compose restart
docker compose down
```

## Nota técnica

El emulador se carga mediante CDN de EmulatorJS:

```text
https://cdn.emulatorjs.org/stable/data/
```

Por eso el navegador necesita internet para cargar el emulador.
