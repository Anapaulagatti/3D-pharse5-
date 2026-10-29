import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createServer } from "node:http";
import { randomBytes, createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
const dir = "docs/review-terms",
  html = await fs.readFile(dir + "/FINAL_REVIEW.html"),
  password = randomBytes(24).toString("hex"),
  auth = "Basic " + Buffer.from("review:" + password).toString("base64");
const server = createServer((req, res) => {
  if (req.headers.authorization !== auth) {
    res.writeHead(401, {
      "WWW-Authenticate": 'Basic realm="private final review"',
    });
    res.end();
    return;
  }
  if (req.url !== "/review") {
    res.writeHead(404);
    res.end();
    return;
  }
  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "Cache-Control": "no-store",
  });
  res.end(html);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}/review`,
  report = {
    checkedAt: new Date().toISOString(),
    status: "RUNNING",
    errors: [],
    external: [],
    actualOwnerExposure: "PENDING",
    termsEvidenceBasis: "OWNER_SUPPLIED_OFFICIAL_PUBLIC_INFORMATION",
    independentOfficialRetrievalVerified: false,
    gameRebuiltOrRerun: false,
  };
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  deviceScaleFactor: 1,
  httpCredentials: { username: "review", password },
  acceptDownloads: true,
});
const page = await context.newPage();
page.on("pageerror", (e) => report.errors.push(e.message));
page.on("request", (r) => {
  if (/^https?:/.test(r.url()) && r.url() !== base)
    report.external.push(r.url());
});
const check = (v, m) => {
  if (!v) throw Error(m);
};
const repository = "/workspace/review-pages-destination",
  fixture = repository + "/review-candidates/contemporary20-qa-only.json";
try {
  await page.goto(base);
  await page.waitForFunction(() => document.body.dataset.ready === "true");
  check(
    (await page.locator("article.card").count()) === 26,
    "Not26private visual records",
  );
  check(
    (await page
      .locator(".pill")
      .filter({ hasText: "INCLUDED · PASS depiction screen" })
      .count()) === 20,
    "Wrong included count",
  );
  check(
    (await page
      .locator(".pill")
      .filter({ hasText: "EXCLUDED · NEEDS REVIEW" })
      .count()) === 6,
    "Wrong excluded count",
  );
  const views = await page.locator(".views img").evaluateAll((images) =>
    images.map((i) => ({
      w: i.naturalWidth,
      h: i.naturalHeight,
      complete: i.complete,
      sampling: getComputedStyle(i).imageRendering,
    })),
  );
  check(
    views.length === 104 &&
      views.every(
        (v) =>
          v.w === 96 && v.h === 112 && v.complete && v.sampling === "pixelated",
      ),
    "Native views altered",
  );
  check(html.length < 1000000, "Page over1MB");
  check(
    await page.locator("#approve").isDisabled(),
    "Approval enabled without owner",
  );
  const manifest = page.waitForEvent("download");
  await page.locator("#download-manifest").click();
  const f = await manifest;
  const file = ".cache/final20-manifest-check.json";
  await f.saveAs(file);
  const hash = createHash("sha256")
    .update(await fs.readFile(file))
    .digest("hex");
  check(
    hash === "bb2c88af58107885cdb12d4097621743274f610a6a9188dd5643aa03cb0ea2b8",
    "Manifest bytes changed",
  );
  report.assetManifestSHA256 = hash;
  const info = page.waitForEvent("download");
  await page.locator("#download-provenance").click();
  const doc = await info;
  const evidenceFile = ".cache/final20-owner-evidence-check.json";
  await doc.saveAs(evidenceFile);
  const data = JSON.parse(await fs.readFile(evidenceFile, "utf8"));
  check(
    data.sources.sourceKind === "OWNER_SUPPLIED_OFFICIAL_PUBLIC_INFORMATION" &&
      data.sources.independentRetrievalVerified === false &&
      data.sources.documents[0].effectiveDate === "2026-01-01" &&
      data.sources.documents[1].effectiveDate ===
        "UNSPECIFIED_IN_OWNER_INFORMATION",
    "Source evidence falsely upgraded",
  );
  await page
    .locator("#owner")
    .fill("SYNTHETIC QA ONLY — NOT AN OWNER DECISION");
  check(await page.locator("#approve").isDisabled(), "Name alone approves");
  await page.locator("#when").fill("2026-10-29T00:00");
  check(
    await page.locator("#approve").isDisabled(),
    "Name/date without acknowledgement approve",
  );
  await page.locator("#ack").check();
  check(
    await page.locator("#approve").isEnabled(),
    "Complete synthetic export not available",
  );
  const receipt = page.waitForEvent("download");
  await page.locator("#approve").click();
  const r = await receipt;
  await r.saveAs(fixture);
  const q = JSON.parse(await fs.readFile(fixture, "utf8"));
  check(
    q.approvedBy.startsWith("SYNTHETIC") &&
      q.decision === "APPROVED_PUBLIC_PREVIEW" &&
      Object.keys(q.npcReviews).length === 20 &&
      q.groups["checkpoint-media"].decision === "NOT_DISTRIBUTED" &&
      q.creationTermsReview.independentOfficialRetrievalVerified === false,
    "Bad complete export",
  );
  const python = `import json,importlib.util\ns=importlib.util.spec_from_file_location('e','tools/review-exposure/eligibility.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);errors=m.validate('.cache/exposure20-private',json.load(open(${JSON.stringify(fixture)})),'docs/review-terms');assert not errors,errors`;
  execFileSync("python3", ["-c", python], {
    cwd: process.cwd(),
    stdio: "pipe",
  });
  for (const args of [
    ["receipt.py", "review-candidates/contemporary20-qa-only.json"],
    [
      "gate.py",
      "/workspace/phase3b-a-recovery/.cache/exposure20-private",
      "review-candidates/contemporary20-qa-only.json",
    ],
    [
      "history_gate.py",
      "/workspace/phase3b-a-recovery/.cache/exposure20-private",
      "review-candidates/contemporary20-qa-only.json",
    ],
  ])
    execFileSync("python3", args, { cwd: repository, stdio: "pipe" });
  await fs.unlink(fixture);
  report.syntheticFixtureDeleted = true;
  report.syntheticFullReceiptLocalAndRepositoryGates =
    "PASS; no push or deployment";
  const actual = JSON.parse(
    await fs.readFile(
      repository + "/review-candidates/contemporary20.json",
      "utf8",
    ),
  );
  check(
    actual.decision === "PENDING" &&
      Object.values(actual.npcReviews).every((r) => r.decision === "PENDING"),
    "Actual owner record changed",
  );
  await page.reload();
  await page.waitForFunction(() => document.body.dataset.ready === "true");
  for (const viewport of [
    { width: 1280, height: 900 },
    { width: 390, height: 844 },
    { width: 667, height: 375 },
  ]) {
    await page.setViewportSize(viewport);
    report.lastLayout = await page.evaluate(() => ({
      width: innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      offenders: [...document.querySelectorAll("body *")]
        .filter((e) => {
          const r = e.getBoundingClientRect();
          return r.width && (r.right > innerWidth + 1 || r.left < -1);
        })
        .slice(0, 12)
        .map((e) => ({
          tag: e.tagName,
          id: e.id,
          cls: e.className,
          text: e.textContent.slice(0, 100),
          right: e.getBoundingClientRect().right,
          left: e.getBoundingClientRect().left,
          width: e.getBoundingClientRect().width,
        })),
    }));
    report.lastLayout.scrollOffenders = await page.evaluate(() =>
      [...document.querySelectorAll("body *")]
        .filter((e) => e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1)
        .map((e) => ({
          tag: e.tagName,
          id: e.id,
          cls: e.className,
          client: e.clientWidth,
          scroll: e.scrollWidth,
          display: getComputedStyle(e).display,
        }))
        .slice(0, 20),
    );
    report.lastLayout.textOverflow = await page.evaluate(() => {
      const w = document.createTreeWalker(
        document.body,
        window.NodeFilter.SHOW_TEXT,
      );
      const a = [];
      while (w.nextNode()) {
        const n = w.currentNode;
        if (["SCRIPT", "STYLE"].includes(n.parentElement?.tagName)) continue;
        const r = document.createRange();
        r.selectNodeContents(n);
        const b = r.getBoundingClientRect();
        if (b.right > innerWidth + 1)
          a.push({
            text: n.textContent.slice(0, 100),
            parent: n.parentElement?.tagName,
            id: n.parentElement?.id,
            right: b.right,
          });
      }
      return a.slice(0, 12);
    });
    check(
      report.lastLayout.documentWidth <= report.lastLayout.width,
      "Layout overflow",
    );
    await page.screenshot({ path: `${dir}/review-${viewport.width}.png` });
  }
  check(
    !report.errors.length && !report.external.length,
    "Unexpected script/network error",
  );
  report.status =
    "PASS FINAL PRIVATE APPROVAL PAGE; ACTUAL OWNER PUBLIC APPROVAL STILL PENDING";
  report.nativeViews = 104;
  report.included = 20;
  report.excluded = 6;
} catch (e) {
  report.status = "FAIL";
  report.failure = e.stack;
  process.exitCode = 1;
} finally {
  await fs.unlink(fixture).catch(() => {});
  await fs.writeFile(
    dir + "/PAGE_QA.json",
    JSON.stringify(report, null, 2) + "\n",
  );
  await browser.close();
  await new Promise((r) => server.close(r));
}
