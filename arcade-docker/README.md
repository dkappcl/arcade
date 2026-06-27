# Arcade Docker Retro

Proyecto portable en Docker para levantar una web de juegos retro en CentOS 9 usando el puerto **8990**.

> Importante: este proyecto no incluye ROMs ni juegos comerciales. Debes copiar únicamente ROMs que tengas derecho legal a usar.

## Estructura

```text
arcade-docker/
├── app/                  # Web FastAPI + frontend
├── roms/arcade/          # Aquí van tus ROMs .zip de arcade/MAME
├── docker-compose.yml
├── Dockerfile
└── scripts/install-centos9.sh
```

## Instalación rápida en CentOS 9

```bash
sudo dnf -y install unzip git curl
unzip arcade-docker.zip
cd arcade-docker
chmod +x scripts/install-centos9.sh
./scripts/install-centos9.sh
```

## Copiar juegos

Copia tus ROMs legales en:

```bash
mkdir -p roms/arcade
cp /ruta/a/tus/roms/*.zip roms/arcade/
```

Ejemplos de nombres MAME comunes:

```text
galaga.zip
galaxian.zip
dkong.zip
junglek.zip
jungleh.zip
pacman.zip
mspacman.zip
1942.zip
1943.zip
frogger.zip
```

## Levantar el servicio

```bash
docker compose up -d --build
```

Abrir en el navegador:

```text
http://IP_DEL_SERVIDOR:8990
```

En el mismo servidor:

```text
http://localhost:8990
```

## Comandos útiles

Ver estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Reiniciar después de agregar ROMs:

```bash
docker compose restart
```

Apagar:

```bash
docker compose down
```

## Firewall CentOS 9

```bash
sudo firewall-cmd --permanent --add-port=8990/tcp
sudo firewall-cmd --reload
```

## Probar salud del servicio

```bash
curl http://localhost:8990/health
```

## Notas

- La web escanea automáticamente `roms/`.
- Los archivos `.zip` y `.7z` se interpretan por defecto como arcade/MAME.
- También se permite crear carpetas `nes/`, `snes/`, `genesis/` si quieres ampliar la biblioteca.
- El reproductor usa EmulatorJS desde CDN, por lo que el navegador necesita internet para cargar el emulador.
