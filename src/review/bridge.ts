/** Private portal build entry only. No change to the canonical game entry. */
const script = document.querySelector<HTMLMetaElement>(
  'meta[name="review-home"]',
);
if (script && import.meta.env.VITE_RELEASE_PROFILE === "private-review") {
  const home = new URL(script.content, location.href);
  if (home.origin !== location.origin)
    throw Error("Review return must be same-origin");
  const scenario = new URLSearchParams(location.search).has("qa");
  if (scenario) {
    // QA demos use separate local/session records. Normal play keeps original keys.
    const get = window.Storage.prototype.getItem;
    const set = window.Storage.prototype.setItem;
    const remove = window.Storage.prototype.removeItem;
    const prefix = "review-only-v1:";
    const scoped = (key: string) =>
      key.startsWith("korean-arena-") ? prefix + key : key;
    window.Storage.prototype.getItem = function (key: string) {
      return get.call(this, scoped(String(key)));
    };
    window.Storage.prototype.setItem = function (key: string, value: string) {
      set.call(this, scoped(String(key)), value);
    };
    window.Storage.prototype.removeItem = function (key: string) {
      remove.call(this, scoped(String(key)));
    };
    try {
      if (!localStorage.getItem("korean-arena-player-preferences-v1"))
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: "juni" }),
        );
    } catch {
      // Keep the original game's in-memory selection fallback when storage is denied.
    }
  }
  const shell = document.createElement("details");
  shell.id = "portal-review-controls";
  shell.style.cssText =
    "position:fixed;top:max(4px,env(safe-area-inset-top));left:max(4px,env(safe-area-inset-left));z-index:10000;background:#172834;color:#fff;padding:6px;border:2px solid #e5b86d;max-width:min(88vw,440px);max-height:75dvh;overflow:auto;font:13px system-ui";
  const toggle = document.createElement("summary");
  toggle.textContent = scenario
    ? "REVIEW ONLY · Công cụ / Trở về"
    : "Review · Trở về";
  toggle.style.cssText = "min-height:44px;cursor:pointer";
  shell.append(toggle);
  const back = document.createElement("a");
  back.href = home.href;
  back.textContent = "← Trở về cổng review";
  back.style.cssText = "display:block;color:#ffe1a1;padding:10px";
  shell.append(back);
  if (scenario) {
    const status = document.createElement("pre");
    status.style.cssText =
      "white-space:pre-wrap;max-width:95%;font:12px monospace";
    shell.append(status);
    const minute = document.createElement("input");
    minute.type = "number";
    minute.min = "0";
    minute.max = "1439";
    minute.value = "540";
    minute.setAttribute("aria-label", "Phút trong ngày REVIEW ONLY");
    const rate = document.createElement("select");
    rate.setAttribute("aria-label", "Tốc độ REVIEW ONLY");
    for (const value of [0, 1, 10, 60]) {
      const o = document.createElement("option");
      o.value = String(value);
      o.textContent = value === 0 ? "Tạm dừng" : `${value}×`;
      rate.append(o);
    }
    rate.value = "1";
    const apply = document.createElement("button");
    apply.textContent = "Đặt giờ · REVIEW ONLY";
    for (const el of [minute, rate, apply])
      el.style.cssText =
        "min-height:44px;max-width:100%;font:inherit;margin:3px";
    apply.addEventListener("click", () =>
      window.__NPC_LIFE_QA__?.setTime(Number(minute.value), Number(rate.value)),
    );
    shell.append(minute, rate, apply);
    const timer = window.setInterval(() => {
      const s = window.__NPC_WORLD__;
      if (s)
        status.textContent =
          `REVIEW ONLY · dữ liệu lưu riêng\nNgày ${s.clock.day} / ${Math.floor(s.clock.minute / 60)}:${String(Math.floor(s.clock.minute % 60)).padStart(2, "0")} · ${s.clock.phase} · ${s.clock.rate}×\nZone: ${s.actors[0]?.zone ?? "—"}\nActors ${s.active}/4 · textures ${s.assets.loaded}/4 · pending ${s.assets.pending}/2\n` +
          s.actors
            .map(
              (a) =>
                `${a.id}: ${a.zone} · ${a.state} · ${a.frame} · ${a.activity?.activity ?? a.activity?.id ?? "—"}`,
            )
            .join("\n");
    }, 500);
    window.addEventListener("pagehide", () => window.clearInterval(timer), {
      once: true,
    });
  }
  document.addEventListener(
    "DOMContentLoaded",
    () => document.body.append(shell),
    { once: true },
  );
}
