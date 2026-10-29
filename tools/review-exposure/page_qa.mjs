import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createServer } from "node:http";
import { randomBytes, createHash } from "node:crypto";
const dir = "docs/review-exposure",
  html = await fs.readFile(dir + "/FINAL_REVIEW.html");
const password = randomBytes(24).toString("hex"),
  auth = "Basic " + Buffer.from("review:" + password).toString("base64");
const server = createServer((req, res) => {
  if (req.headers.authorization !== auth) {
    res.writeHead(401, { "WWW-Authenticate": 'Basic realm="private review"' });
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
    ownerExposure: "NOT APPROVED",
    terms: "UNKNOWN",
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
const check = (a, m) => {
  if (!a) throw Error(m);
};
try {
  await page.goto(base);
  await page.waitForFunction(() => document.body.dataset.ready === "true");
  check(
    (await page.locator("article.card").count()) === 26,
    "26 native private comparison records missing",
  );
  const views = await page.locator(".views img").evaluateAll((images) =>
    images.map((i) => ({
      w: i.naturalWidth,
      h: i.naturalHeight,
      ok: i.complete,
      sampling: getComputedStyle(i).imageRendering,
    })),
  );
  check(
    views.length === 104 &&
      views.every(
        (v) => v.w === 96 && v.h === 112 && v.ok && v.sampling === "pixelated",
      ),
    "Native views broken",
  );
  check(
    (await page
      .locator(".pill")
      .filter({ hasText: "INCLUDED · PASS depiction screen" })
      .count()) === 20,
    "Incorrect contemporary screen",
  );
  check(
    (await page
      .locator(".pill")
      .filter({ hasText: "EXCLUDED · NEEDS REVIEW" })
      .count()) === 6,
    "Incorrect exclusion labels",
  );
  check(
    await page.locator("#approve").isDisabled(),
    "UNKNOWN approval enabled",
  );
  check(html.length < 1000000, "Page heavier than1MB");
  const download = page.waitForEvent("download");
  await page.locator("#download-manifest").click();
  const downloaded = await download;
  const tmp = ".cache/exposure20-manifest-download.json";
  await downloaded.saveAs(tmp);
  const got = createHash("sha256")
    .update(await fs.readFile(tmp))
    .digest("hex");
  const expected = JSON.parse(
    await fs.readFile(dir + "/RESTRICTED20_PACKAGE.json", "utf8"),
  ).manifestSHA256;
  check(got === expected, "Exact manifest download differs");
  report.manifestSHA256 = got;
  await page.locator("#service").fill("SYNTHETIC UI TEST ONLY");
  await page.locator("#terms").fill("UNKNOWN — this input is not permission");
  await page.locator("#authority").fill("No actual owner evidence supplied");
  const response = page.waitForEvent("download");
  await page.locator("#response").click();
  const f = await response;
  const tmpResponse = ".cache/synthetic-evidence-response.json";
  await f.saveAs(tmpResponse);
  const q = JSON.parse(await fs.readFile(tmpResponse, "utf8"));
  check(
    q.decision === "EVIDENCE_SUBMITTED_FOR_REVIEW_NOT_PUBLIC_APPROVAL" &&
      q.termsStatus === "UNVERIFIED_PENDING_INSPECTION",
    "Response falsely clears rights",
  );
  await fs.unlink(tmpResponse);
  check(
    await page.locator("#approve").isDisabled(),
    "Evidence text falsely enables permission",
  );
  await page.reload();
  await page.waitForFunction(() => document.body.dataset.ready === "true");
  for (const viewport of [
    { width: 1280, height: 900 },
    { width: 390, height: 844 },
    { width: 667, height: 375 },
  ]) {
    await page.setViewportSize(viewport);
    check(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      "Layout overflow",
    );
    await page.screenshot({ path: `${dir}/review-${viewport.width}.png` });
  }
  check(
    !report.errors.length && !report.external.length,
    "Script/network error",
  );
  report.status = "PASS PRIVATE REVIEW PAGE; NO PUBLIC APPROVAL";
  report.records = 26;
  report.included = 20;
  report.excluded = 6;
  report.nativeViews = 104;
  report.syntheticFixtureDeleted = true;
} catch (e) {
  report.status = "FAIL";
  report.failure = e.stack;
  process.exitCode = 1;
} finally {
  await fs.writeFile(
    dir + "/PAGE_QA.json",
    JSON.stringify(report, null, 2) + "\n",
  );
  await browser.close();
  await new Promise((r) => server.close(r));
}
