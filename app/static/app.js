let items = [];

const controls = ["maxWeight", "heat", "rain"];

function value(id) {
  return Number(document.getElementById(id).value);
}

function syncOutputs() {
  for (const id of controls) {
    document.getElementById(`${id}Out`).textContent = value(id);
  }
}

function renderItems(selectedIds = []) {
  const selected = new Set(selectedIds);
  document.getElementById("items").innerHTML = items.map((item) => `
    <article class="item ${selected.has(item.id) ? "chosen" : ""}">
      <div>
        <strong>${item.name}</strong>
        <small>${item.id}</small>
      </div>
      <dl>
        <div><dt>weight</dt><dd>${item.weight}</dd></div>
        <div><dt>happy</dt><dd>${item.happiness}</dd></div>
        <div><dt>heat</dt><dd>-${item.heat_penalty}</dd></div>
        <div><dt>rain</dt><dd>-${item.rain_penalty}</dd></div>
      </dl>
    </article>
  `).join("");
}

async function optimize() {
  syncOutputs();
  const res = await fetch("/api/optimize", {
    method: "POST",
    headers: {"content-type": "application/json"},
    body: JSON.stringify({
      items,
      constraints: {
        max_weight: value("maxWeight"),
        heat: value("heat"),
        rain: value("rain")
      }
    })
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.error);
  const result = data.result;
  renderItems(result.selected_ids);
  document.getElementById("score").textContent = result.score;
  document.getElementById("selected").innerHTML = `
    <p><strong>${result.total_weight}</strong> total weight</p>
    <p>${result.selected_ids.length ? result.selected_ids.join(", ") : "empty basket"}</p>
  `;
  document.getElementById("warnings").innerHTML = result.warnings
    .map((warning) => `<p>${warning}</p>`)
    .join("");
}

async function init() {
  const res = await fetch("/api/items");
  items = (await res.json()).items;
  renderItems();
  for (const id of controls) {
    document.getElementById(id).addEventListener("input", optimize);
  }
  await optimize();
}

init().catch((err) => {
  document.body.innerHTML = `<pre>${err.stack || err}</pre>`;
});
