let allGames = [];
let currentSystem = "all";
const statusEl = document.getElementById("status");
const gamesEl = document.getElementById("games");
const countEl = document.getElementById("gameCount");
const searchEl = document.getElementById("search");

async function api(path, options={}) {
  const res = await fetch(path, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
async function loadGames() {
  try {
    await api("/api/health");
    statusEl.textContent = "API OK";
    const data = await api("/api/games");
    allGames = data.games || [];
    countEl.textContent = allGames.length;
    render();
  } catch (err) {
    statusEl.textContent = "API sin conexión";
    gamesEl.innerHTML = `<div class="panel">No se pudo conectar con la API: ${err.message}</div>`;
  }
}
function render() {
  const q = searchEl.value.toLowerCase().trim();
  let filtered = allGames.filter(g => currentSystem === "all" || g.system === currentSystem);
  if (q) filtered = filtered.filter(g => g.name.toLowerCase().includes(q) || g.file.toLowerCase().includes(q));
  if (!filtered.length) {
    gamesEl.innerHTML = `<div class="panel">No hay juegos detectados. Sube una ROM legal desde el panel lateral.</div>`;
    return;
  }
  gamesEl.innerHTML = filtered.map(g => `
    <div class="card">
      <div>
        <span class="badge">${g.system.toUpperCase()}</span>
        <h4>${g.name}</h4>
        <div class="meta">${g.file}</div>
        <div class="meta">${g.size_mb} MB</div>
      </div>
      <div class="actions">
        <a class="play" href="${g.play_url}">▶ Jugar</a>
        <a href="${g.url}" target="_blank">Archivo</a>
      </div>
    </div>`).join("");
}
document.querySelectorAll(".system").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".system").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentSystem = btn.dataset.system;
    render();
  });
});
searchEl.addEventListener("input", render);
document.getElementById("refresh").addEventListener("click", loadGames);
document.getElementById("uploadForm").addEventListener("submit", async e => {
  e.preventDefault();
  const file = document.getElementById("romFile").files[0];
  const system = document.getElementById("uploadSystem").value;
  if (!file) return alert("Selecciona una ROM legal.");
  const form = new FormData();
  form.append("system", system);
  form.append("file", file);
  try {
    const res = await api("/api/upload", { method: "POST", body: form });
    document.getElementById("romFile").value = "";
    await loadGames();
    if (confirm("ROM subida correctamente. ¿Quieres jugar ahora?")) window.location.href = res.play_url;
  } catch (err) {
    alert("Error al subir: " + err.message);
  }
});
loadGames();
