import os
import json
from pathlib import Path
from typing import List, Dict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"
ROMS_DIR = Path(os.getenv("ARCADE_ROMS_DIR", "/data/roms"))
TITLE = os.getenv("ARCADE_TITLE", "Arcade Docker Retro")

SUPPORTED_EXTENSIONS = {".zip", ".7z", ".nes", ".sfc", ".smc", ".bin", ".rom"}
ARCADE_EXTENSIONS = {".zip", ".7z"}

SYSTEM_BY_FOLDER = {
    "arcade": "arcade",
    "mame": "arcade",
    "nes": "nes",
    "snes": "snes",
    "genesis": "segaMD",
    "megadrive": "segaMD",
}

FRIENDLY_NAMES = {
    "galaga": "Galaga",
    "galaxian": "Galaxian",
    "dkong": "Donkey Kong",
    "dkongjr": "Donkey Kong Jr.",
    "junglek": "Jungle King",
    "jungleh": "Jungle Hunt",
    "pacman": "Pac-Man",
    "mspacman": "Ms. Pac-Man",
    "spaceinv": "Space Invaders",
    "frogger": "Frogger",
    "asteroid": "Asteroids",
    "centiped": "Centipede",
    "digdug": "Dig Dug",
    "1942": "1942",
    "1943": "1943",
    "xevious": "Xevious",
    "defender": "Defender",
    "phoenix": "Phoenix",
    "scramble": "Scramble",
    "bombjack": "Bomb Jack",
}

def guess_core(path: Path) -> str:
    folder = path.parent.name.lower()
    if folder in SYSTEM_BY_FOLDER:
        return SYSTEM_BY_FOLDER[folder]
    if path.suffix.lower() in ARCADE_EXTENSIONS:
        return "arcade"
    return "nes"


def display_name(path: Path) -> str:
    stem = path.stem.lower()
    return FRIENDLY_NAMES.get(stem, path.stem.replace("_", " ").replace("-", " ").title())


def scan_roms() -> List[Dict[str, str]]:
    games = []
    if not ROMS_DIR.exists():
        return games
    for file in sorted(ROMS_DIR.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        rel = file.relative_to(ROMS_DIR).as_posix()
        games.append({
            "id": rel.replace("/", "__"),
            "name": display_name(file),
            "file": rel,
            "system": guess_core(file),
            "url": f"/roms/{rel}",
            "size_mb": round(file.stat().st_size / 1024 / 1024, 2),
        })
    return games

app = FastAPI(title=TITLE)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/roms", StaticFiles(directory=ROMS_DIR), name="roms")

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    games = scan_roms()
    template = env.get_template("index.html")
    return template.render(title=TITLE, games=games, total=len(games))

@app.get("/api/games")
def api_games():
    return JSONResponse(scan_roms())

@app.get("/play/{game_id}", response_class=HTMLResponse)
def play(game_id: str):
    games = scan_roms()
    game = next((g for g in games if g["id"] == game_id), None)
    if not game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    template = env.get_template("play.html")
    return template.render(title=TITLE, game=game, game_json=json.dumps(game))

@app.get("/health")
def health():
    return {"status": "ok", "roms_dir": str(ROMS_DIR), "games": len(scan_roms())}
