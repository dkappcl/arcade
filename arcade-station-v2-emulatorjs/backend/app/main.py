from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from datetime import datetime

app = FastAPI(title="Arcade Station API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BASE = Path("/data")
ROMS = BASE / "roms"
METADATA = BASE / "metadata"
ALLOWED_SYSTEMS = ["arcade", "nes", "snes", "sega", "neogeo", "atari", "gba", "gb", "gbc"]
ALLOWED_EXT = {".zip", ".nes", ".sfc", ".smc", ".gen", ".md", ".bin", ".a26", ".gba", ".gb", ".gbc"}
CORE_BY_SYSTEM = {"nes":"nes","snes":"snes","sega":"segaMD","atari":"atari2600","gba":"gba","gb":"gb","gbc":"gb","arcade":"arcade","neogeo":"arcade"}

def ensure_dirs():
    for system in ALLOWED_SYSTEMS:
        (ROMS / system).mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)

def safe_name(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in "._- ()[]").strip()

def scan_games():
    ensure_dirs()
    games = []
    for system in ALLOWED_SYSTEMS:
        folder = ROMS / system
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix.lower() in ALLOWED_EXT:
                games.append({
                    "name": path.stem.replace("_", " ").replace("-", " ").title(),
                    "file": path.name,
                    "system": system,
                    "core": CORE_BY_SYSTEM.get(system, system),
                    "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
                    "updated": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                    "url": f"/roms/{system}/{path.name}",
                    "play_url": f"/player.html?system={system}&file={path.name}"
                })
    return games

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Arcade Station API", "version": "2.0.0"}

@app.get("/api/systems")
def systems():
    return {"systems": ALLOWED_SYSTEMS, "cores": CORE_BY_SYSTEM}

@app.get("/api/games")
def games():
    return {"games": scan_games()}

@app.post("/api/upload")
async def upload_rom(system: str = Form(...), file: UploadFile = File(...)):
    ensure_dirs()
    if system not in ALLOWED_SYSTEMS:
        raise HTTPException(status_code=400, detail="Sistema no permitido")
    filename = safe_name(file.filename or "")
    if not filename:
        raise HTTPException(status_code=400, detail="Archivo inválido")
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Extensión no permitida: {ext}")
    dest = ROMS / system / filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"ok": True, "system": system, "file": filename, "play_url": f"/player.html?system={system}&file={filename}"}
