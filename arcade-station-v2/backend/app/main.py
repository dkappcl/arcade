from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from datetime import datetime

app = FastAPI(title="Arcade Station API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BASE = Path("/data")
ROMS = BASE / "roms"
COVERS = BASE / "covers"

SYSTEMS = {
    "arcade": {"label": "Arcade / MAME", "core": "arcade", "extensions": [".zip"]},
    "neogeo": {"label": "Neo Geo", "core": "arcade", "extensions": [".zip"]},
    "nes": {"label": "NES", "core": "nes", "extensions": [".nes", ".zip"]},
    "snes": {"label": "SNES", "core": "snes", "extensions": [".sfc", ".smc", ".zip"]},
    "sega": {"label": "Sega Genesis / Mega Drive", "core": "segaMD", "extensions": [".gen", ".md", ".bin", ".zip"]},
    "atari": {"label": "Atari 2600", "core": "atari2600", "extensions": [".a26", ".bin", ".zip"]},
    "gb": {"label": "Game Boy", "core": "gb", "extensions": [".gb", ".zip"]},
    "gbc": {"label": "Game Boy Color", "core": "gb", "extensions": [".gbc", ".zip"]},
    "gba": {"label": "Game Boy Advance", "core": "gba", "extensions": [".gba", ".zip"]},
}

def ensure_dirs():
    for system in SYSTEMS:
        (ROMS / system).mkdir(parents=True, exist_ok=True)
        (COVERS / system).mkdir(parents=True, exist_ok=True)

def safe_name(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in "._- ()[]").strip()

def human_name(stem: str) -> str:
    return stem.replace("_"," ").replace("-"," ").replace("."," ").title()

def cover_for(system: str, stem: str):
    for ext in [".png",".jpg",".jpeg",".webp"]:
        p = COVERS / system / f"{stem}{ext}"
        if p.exists():
            return f"/covers/{system}/{p.name}"
    return None

def scan_games():
    ensure_dirs()
    games = []
    for system, cfg in SYSTEMS.items():
        for path in sorted((ROMS / system).iterdir()):
            if path.is_file() and path.suffix.lower() in cfg["extensions"]:
                name = human_name(path.stem)
                games.append({
                    "id": f"{system}:{path.name}",
                    "name": name,
                    "file": path.name,
                    "system": system,
                    "system_label": cfg["label"],
                    "core": cfg["core"],
                    "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
                    "updated": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                    "url": f"/roms/{system}/{path.name}",
                    "cover": cover_for(system, path.stem),
                    "play_url": f"/player.html?system={system}&core={cfg['core']}&rom=/roms/{system}/{path.name}&name={name}"
                })
    return games

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Arcade Station API", "version": "2.0.0"}

@app.get("/api/systems")
def systems():
    return {"systems": [{"id": k, **v} for k, v in SYSTEMS.items()]}

@app.get("/api/games")
def games():
    return {"games": scan_games()}

@app.post("/api/upload")
async def upload_rom(system: str = Form(...), file: UploadFile = File(...)):
    ensure_dirs()
    if system not in SYSTEMS:
        raise HTTPException(status_code=400, detail="Sistema no permitido")
    filename = safe_name(file.filename or "")
    ext = Path(filename).suffix.lower()
    if ext not in SYSTEMS[system]["extensions"]:
        raise HTTPException(status_code=400, detail=f"Extensión no permitida para {system}: {ext}")
    dest = ROMS / system / filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"ok": True, "system": system, "file": filename}

@app.post("/api/upload-cover")
async def upload_cover(system: str = Form(...), rom_name: str = Form(...), file: UploadFile = File(...)):
    ensure_dirs()
    if system not in SYSTEMS:
        raise HTTPException(status_code=400, detail="Sistema no permitido")
    stem = Path(safe_name(rom_name)).stem
    filename = safe_name(file.filename or "")
    ext = Path(filename).suffix.lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        raise HTTPException(status_code=400, detail="Carátula debe ser png, jpg, jpeg o webp")
    dest = COVERS / system / f"{stem}{ext}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"ok": True, "cover": f"/covers/{system}/{dest.name}"}

@app.delete("/api/games/{system}/{filename}")
def delete_game(system: str, filename: str):
    if system not in SYSTEMS:
        raise HTTPException(status_code=400, detail="Sistema no permitido")
    path = ROMS / system / safe_name(filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    path.unlink()
    return {"ok": True}
