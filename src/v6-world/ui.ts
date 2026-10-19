import type Phaser from "phaser";
import { FullWorld, worldAssetRoot, worldSize } from "../v3-world/World";
import { attachJoystick } from "../full-world/Joystick";
import { controls } from "../game/Plaza";
import {
  letterLesson,
  parseAcademyProgress,
  progressKey,
} from "../domains/academy";
export function setupFullUI(game: Phaser.Game) {
  const $ = <T extends HTMLElement = HTMLElement>(id: string) =>
    document.getElementById(id) as T;
  const scene = () => game.scene.getScenes(true)[0] as FullWorld;
  let ready = false;
  let manualPause = false;
  let resetStick = () => {};
  const runners = new Set<number>();
  const portrait = () =>
    matchMedia("(pointer: coarse)").matches && innerHeight > innerWidth;
  function resetInput() {
    resetStick();
    runners.clear();
    controls.x = 0;
    controls.y = 0;
    controls.run = false;
    $("run").setAttribute("aria-pressed", "false");
  }
  function syncPause() {
    const rotated = portrait();
    $("rotate-screen").hidden = !rotated;
    controls.paused =
      !ready ||
      manualPause ||
      rotated ||
      document.hidden ||
      !$("settings").hidden ||
      !$("dialog").hidden;
    if (controls.paused) resetInput();
    $("pause").textContent = manualPause ? "Tiếp tục" : "Tạm dừng";
    $("pause").setAttribute("aria-pressed", String(manualPause));
  }
  $("pause").onclick = () => {
    manualPause = !manualPause;
    syncPause();
  };
  $("settings-open").onclick = () => {
    $("settings").hidden = false;
    syncPause();
  };
  $("settings-close").onclick = () => {
    $("settings").hidden = true;
    syncPause();
    game.canvas.focus();
  };
  for (const event of ["resize", "orientationchange", "focus", "blur"])
    window.addEventListener(event, () => {
      resetInput();
      syncPause();
    });
  document.addEventListener("visibilitychange", syncPause);
  document.addEventListener("fullscreenchange", syncPause);
  const orientation = async () => {
    let detail: string;
    try {
      if (
        !document.fullscreenElement &&
        document.documentElement.requestFullscreen
      )
        await document.documentElement.requestFullscreen();
      const o = screen.orientation as ScreenOrientation & {
        lock?: (mode: string) => Promise<void>;
      };
      if (!o?.lock) throw new Error("unsupported");
      await o.lock("landscape");
      detail =
        "Đã yêu cầu chế độ ngang. Bố cục sẽ theo chiều màn hình thực tế.";
    } catch {
      detail =
        "Trình duyệt không khóa được chiều màn hình. Hãy xoay ngang thiết bị và tắt khóa xoay; game sẽ tự tiếp tục.";
    }
    $("orientation-status").textContent = detail;
    $("rotate-note").textContent = detail;
    syncPause();
  };
  $("fullscreen").onclick = () => void orientation();
  $("enter-landscape").onclick = () => void orientation();
  if (matchMedia("(pointer: coarse)").matches)
    $("interact").textContent = "Khám phá";
  controls.zoom = 1;
  $("zoom").onchange = (e) => {
    controls.zoom = Number((e.target as HTMLSelectElement).value);
  };
  const reduced = $("motion") as HTMLInputElement;
  reduced.checked = controls.reduced;
  reduced.onchange = () => {
    controls.reduced = reduced.checked;
  };
  matchMedia("(prefers-reduced-motion: reduce)").addEventListener(
    "change",
    (e) => {
      controls.reduced = e.matches;
      reduced.checked = e.matches;
    },
  );
  $("night").onclick = () => {
    controls.night = !controls.night;
    $("night").setAttribute("aria-pressed", String(controls.night));
  };
  const sizes = $("control-size") as HTMLSelectElement;
  try {
    const saved = localStorage.getItem("korean-arena-control-size");
    if (saved === "56" || saved === "68") sizes.value = saved;
  } catch {
    /* session only */
  }
  const applySize = () => {
    document.documentElement.style.setProperty("--control", sizes.value + "px");
    try {
      localStorage.setItem("korean-arena-control-size", sizes.value);
    } catch {
      /* session only */
    }
  };
  sizes.onchange = applySize;
  applySize();
  resetStick = attachJoystick(
    $("joystick"),
    (x, y) => {
      controls.x = x;
      controls.y = y;
    },
    () => controls.paused,
  );
  window.addEventListener("full-reset-input", resetInput);
  window.addEventListener("full-loading", () => {
    ready = false;
    syncPause();
  });
  $("emote").onclick = () => {
    $("emote-menu").hidden = !$("emote-menu").hidden;
    $("emote").setAttribute("aria-expanded", String(!$("emote-menu").hidden));
  };
  $("talk").onclick = () => {
    if (!ready) return;
    if (!$("dialog").hidden) {
      const next = $("dialog-copy").querySelector<HTMLButtonElement>(
        "button[data-continue]",
      );
      if (next) next.click();
      else $("close-dialog").click();
    } else scene().interact();
  };
  $("mini-wrap").onclick = () => {
    say(
      "Hành trình Hàn Quốc hư cấu · Đi bộ theo phố/vườn giữa di sản, rừng tháp, công viên hoa và ga ven biển. Bến phà nối vườn Jeju. Các nơi ngoài đời ở những vùng khác nhau.",
    );
    const img = document.createElement("img");
    img.src = import.meta.env.BASE_URL + worldAssetRoot + "minimap.png";
    img.alt = "Toàn bản đồ năm vùng chơi được";
    img.className = "journey-map";
    $("dialog-copy").append(img);
  };
  const run = $("run");
  run.onpointerdown = (e) => {
    e.preventDefault();
    if (controls.paused) return;
    run.setPointerCapture(e.pointerId);
    runners.add(e.pointerId);
    controls.run = true;
    run.setAttribute("aria-pressed", "true");
  };
  const stopRun = (e: PointerEvent) => {
    runners.delete(e.pointerId);
    controls.run = runners.size > 0;
    run.setAttribute("aria-pressed", String(controls.run));
  };
  run.onpointerup = stopRun;
  run.onpointercancel = stopRun;
  run.onlostpointercapture = stopRun;
  for (const action of ["wave", "celebrate"] as const)
    $(action).onclick = () => {
      if (ready) {
        scene().emote(action);
        $("emote-menu").hidden = true;
        $("emote").setAttribute("aria-expanded", "false");
      }
    };
  $("interact").onclick = () => {
    if (ready) scene().interact();
  };
  $("close-dialog").onclick = () => {
    $("dialog").hidden = true;
    syncPause();
    game.canvas.focus();
  };
  new MutationObserver(syncPause).observe($("dialog"), {
    attributes: true,
    attributeFilter: ["hidden"],
  });
  function say(message: string) {
    $("dialog-copy").textContent = message;
    $("dialog").hidden = false;
    syncPause();
  }
  window.addEventListener("town-dialog", (e) =>
    say((e as CustomEvent<string>).detail),
  );
  window.addEventListener("v3-discovery", () => {
    say(
      "현무암 · Basalt. Quan sát ba mẫu đá ở sân. Vật liệu nào được hình thành khi dung nham nguội đi?",
    );
    const feedback = document.createElement("p");
    feedback.id = "discovery-feedback";
    feedback.setAttribute("role", "status");
    for (const [name, correct] of [
      ["현무암 · Đá basalt", true],
      ["한지 · Giấy hanji", false],
      ["청동 · Đồng", false],
    ] as const) {
      const button = document.createElement("button");
      button.textContent = name;
      button.dataset.discovery = String(correct);
      button.onclick = () => {
        if (!correct) {
          feedback.textContent =
            "Chưa đúng. Hãy nhìn các lỗ rỗng trên mẫu đá: chúng gợi những bọt khí trong dung nham.";
          return;
        }
        (scene() as FullWorld).completeDiscovery();
        feedback.textContent =
          "발견! · Đã khám phá. Basalt hình thành từ dung nham nguội. Đá núi lửa, tường chắn gió và vườn quýt gắn với cảnh quan Jeju.";
        $("dialog-copy")
          .querySelectorAll<HTMLButtonElement>("button[data-discovery]")
          .forEach((b) => (b.disabled = true));
      };
      $("dialog-copy").append(button);
    }
    $("dialog-copy").append(feedback);
  });
  window.addEventListener("full-ferry", (e) => {
    const to = (e as CustomEvent<"jeju" | "busan-coast">).detail;
    say(
      to === "jeju"
        ? "배 · Phà. Jeju và Busan xa nhau ngoài đời. Chuyến phà trong bản đồ du lịch giáo dục này là chuyển tiếp hư cấu, không mô phỏng một tuyến thật."
        : "배 · Phà. Trở lại ga và đường dạo Blue Letter Coast.",
    );
    const go = document.createElement("button");
    go.id = "travel-go";
    go.dataset.continue = "true";
    go.textContent =
      to === "jeju" ? "Lên phà đến Windstone" : "Lên phà về bờ biển";
    go.onclick = () => {
      $("dialog").hidden = true;
      syncPause();
      resetInput();
      (scene() as FullWorld).ferry(to);
    };
    $("dialog-copy").append(go);
  });
  window.addEventListener("game-ready", () => {
    ready = true;
    $("loading")?.remove();
    if ($("settings").hidden && $("dialog").hidden && !portrait())
      game.canvas.focus();
    $("travel-veil").hidden = true;
    $("render-status").textContent = "Hành trình đã sẵn sàng · Chơi cục bộ";
    syncPause();
  });
  window.addEventListener("game-error", (e) => {
    $("render-status").textContent = (e as CustomEvent<string>).detail;
  });
  let progress = parseAcademyProgress(null);
  try {
    progress = parseAcademyProgress(localStorage.getItem(progressKey));
  } catch {
    /* preserve lesson in session */
  }
  const status = () => {
    $("quest-progress").textContent = progress.mastered.length
      ? `Hangul · ${progress.mastered.length}/3 tên chữ đã khám phá`
      : matchMedia("(pointer: coarse)").matches
        ? "Kéo cần để đi · Giữ Chạy · Chạm Khám phá"
        : "WASD / ↑↓←→ · Shift chạy · E khám phá";
  };
  status();
  window.addEventListener("district-position", (e) => {
    const p = (
      e as CustomEvent<{ area: string; x: number; y: number; location: string }>
    ).detail;
    $("district-location").textContent = p.location;
    const room = p.area === "room";
    const map = $("mini-map") as HTMLImageElement;
    map.alt = "Bản đồ di sản, Namsan, Bora Bloom, bờ biển và Windstone";
    $("map-player").style.left =
      ((room ? 1568 : p.x) / worldSize[0]) * 100 + "%";
    $("map-player").style.top =
      ((room ? 1152 : p.y) / worldSize[1]) * 100 + "%";
  });
  let index = 0;
  const render = () => {
    const copy = $("dialog-copy");
    copy.replaceChildren();
    const title = document.createElement("strong");
    title.textContent =
      index < 3 ? `Bàn học Hangul · ${index + 1}/3` : "Hoàn thành bài đầu!";
    copy.append(title);
    if (index === 3) {
      const p = document.createElement("p");
      p.textContent =
        "Bạn đã ghép ㄱ—giyeok, ㄴ—nieun, ㅁ—mieum. Đây là tên chữ; cách đọc trong từ sẽ học ở bước sau.";
      copy.append(p);
      return;
    }
    const item = letterLesson[index];
    const question = document.createElement("p");
    question.innerHTML = `<span class="hangul-letter">${item.glyph}</span>Chọn tên chữ này:`;
    copy.append(question);
    const feedback = document.createElement("p");
    feedback.setAttribute("role", "status");
    for (const name of ["mieum", "giyeok", "nieun"]) {
      const b = document.createElement("button");
      b.textContent = name;
      b.onclick = () => {
        if (name !== item.name) {
          feedback.textContent = "Chưa đúng. Hãy quan sát nét chữ và thử lại.";
          return;
        }
        progress.mastered = [...new Set([...progress.mastered, item.glyph])];
        try {
          localStorage.setItem(progressKey, JSON.stringify(progress));
        } catch {
          $("storage-status").textContent =
            "Lưu trữ không khả dụng; kết quả giữ trong phiên này.";
        }
        status();
        copy.querySelectorAll("button").forEach((b) => (b.disabled = true));
        feedback.textContent = item.vi;
        const next = document.createElement("button");
        next.dataset.continue = "true";
        next.textContent = index === 2 ? "Hoàn thành" : "Chữ tiếp theo";
        next.onclick = () => {
          index++;
          render();
        };
        copy.append(next);
      };
      copy.append(b);
    }
    copy.append(feedback);
  };
  window.addEventListener("academy-lesson", () => {
    index = 0;
    render();
    $("dialog").hidden = false;
    syncPause();
    $("dialog-copy").querySelector<HTMLButtonElement>("button")?.focus();
  });
  game.canvas.tabIndex = 0;
  syncPause();
}
