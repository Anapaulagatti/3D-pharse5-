const el = (tag, text, cls) => {
  const n = document.createElement(tag);
  if (text) n.textContent = text;
  if (cls) n.className = cls;
  return n;
};
async function read(path) {
  const r = await fetch(path, { cache: "no-store" });
  if (!r.ok) throw Error(`${path}: ${r.status}`);
  return r.json();
}
try {
  const [version, data, qa, history] = await Promise.all(
    ["version.json", "catalog.json", "qa.json", "history.json"].map(read),
  );
  document.querySelector("#version").textContent =
    `${version.phase} · ${version.gameCommit.slice(0, 8)} · portal ${version.portalCommit.slice(0, 8)} · build ${new Date(version.builtAt).toLocaleString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" })} (Việt Nam)`;
  for (const [name, value] of Object.entries({
    "ARTISTIC REVIEW": "PENDING",
    "TECHNICAL QA": qa.status,
    "COMMERCIAL RELEASE": "BLOCKED_PENDING_REVIEW",
    "PHYSICAL ANDROID / iPHONE / GPU": "NOT TESTED",
  })) {
    const card = el("div", null, "card");
    card.append(el("small", name), el("p", value));
    document.querySelector("#statuses").append(card);
  }
  document.querySelector("#qa-summary").textContent = qa.summary;
  const roster = document.querySelector("#roster");
  function render(search = "") {
    roster.replaceChildren();
    for (const n of data.npcs.filter((n) =>
      `${n.name.vi} ${n.name.ko} ${n.zone}`
        .toLowerCase()
        .includes(search.toLowerCase()),
    )) {
      const c = el("article", null, "card");
      const img = el("img", null, "sprite");
      img.src = `thumbs/${n.id}.png`;
      img.alt = `${n.name.vi} · native 96×112`;
      img.width = 96;
      img.height = 112;
      img.loading = "lazy";
      c.append(
        img,
        el("h3", `${n.name.vi} · ${n.name.ko}`),
        el("p", `${n.zone} · ${n.role}`),
      );
      const d = el("details");
      d.append(el("summary", "Lịch / chi tiết"));
      if (n.archive)
        d.append(
          el(
            "p",
            "Nhân vật truyện xưa hư cấu · thay thế host slot · không phải người lịch sử thật.",
          ),
        );
      for (const entry of n.schedule)
        d.append(
          el(
            "p",
            `${entry.phase}: ${entry.activity} · ${entry.id.replace(n.id + "-", "")}`,
          ),
        );
      const link = el("a", "Tiếp cận NPC · REVIEW ONLY", "button");
      link.href = `play/?qa&npcReview=${encodeURIComponent(n.id)}`;
      c.append(d, link);
      roster.append(c);
    }
  }
  render();
  document
    .querySelector("#search")
    .addEventListener("input", (e) => render(e.target.value));
  for (const n of data.npcs)
    document
      .querySelector("#rights")
      .append(
        el(
          "p",
          `${n.name.vi} / ${n.name.ko}: ${n.risk} · ${n.publication}. Điều khoản tạo art: UNKNOWN. Public exposure: NOT APPROVED.`,
        ),
      );
  for (const pair of data.comparisons) {
    const c = el("article", null, "card");
    c.append(el("h3", pair.title));
    const row = el("div", null, "pair");
    for (const [label, file] of [
      ["Trước · Phase 3A", pair.before],
      ["Hiện tại · Phase 3B-A", pair.after],
    ]) {
      const f = el("figure"),
        img = el("img", null, "sprite");
      img.src = file;
      img.alt = `${pair.title} ${label} · native`;
      img.loading = "lazy";
      img.width = 96;
      img.height = 112;
      f.append(img, el("figcaption", label));
      row.append(f);
    }
    c.append(
      row,
      el(
        "p",
        "Sprite pixel-identical. Chỉ hành vi thay đổi; không tái tạo artwork.",
      ),
    );
    document.querySelector("#comparisons").append(c);
  }
  for (const movie of data.movies) {
    const c = el("article", null, "card"),
      button = el("button", "Tải video checkpoint khi cần");
    c.append(el("h3", movie.title), button);
    button.addEventListener("click", () => {
      const v = el("video");
      v.controls = true;
      v.preload = "none";
      v.src = movie.file;
      v.setAttribute("playsinline", "");
      c.replaceChild(v, button);
    });
    document.querySelector("#movies").append(c);
  }
  document.querySelector("#snapshot-label").textContent = version.archived
    ? `SNAPSHOT · ${version.gameCommit.slice(0, 8)} · không phải trang current.`
    : "CURRENT · chỉ chuyển phiên bản bằng thao tác promotion rõ ràng.";
  for (const h of history.snapshots) {
    const a = el("a", `${h.phase} · ${h.sha.slice(0, 8)} · snapshot`, "button");
    a.href = h.path;
    document.querySelector("#history-list").append(a);
  }
  const back = el("a", "Về phiên bản current", "button");
  back.href = version.currentPath;
  document.querySelector("#history-list").append(back);
  document.querySelector("#copy").addEventListener("click", async () => {
    const text = `Korean Pixel Town — ${version.phase}\nGame SHA: ${version.gameCommit}\nPortal SHA: ${version.portalCommit}\nBuild: ${version.builtAt}\nBrowser: ${navigator.userAgent}\nViewport: ${document.documentElement.clientWidth}×${document.documentElement.clientHeight}\nPath: ${location.pathname}\nSteps / Expected / Actual:\n${document.querySelector("#steps").value}`;
    document.querySelector("#report").value = text;
    try {
      await navigator.clipboard.writeText(text);
      document.querySelector("#copy-status").textContent = "Đã sao chép.";
    } catch {
      document.querySelector("#report").select();
      document.querySelector("#copy-status").textContent =
        "Chọn và sao chép nội dung bên dưới.";
    }
  });
} catch (error) {
  document.querySelector("#version").textContent =
    `Không tải được review: ${error.message}`;
}
