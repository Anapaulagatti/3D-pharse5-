import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createServer } from "node:http";
import { createHash, randomBytes } from "node:crypto";
const dir = "docs/review-final";
const report = {
  status: "RUNNING",
  checkedAt: new Date().toISOString(),
  rows: [],
  errors: [],
  externalRequests: [],
  realOwnerDecision: "PENDING",
  publication: "NOT DEPLOYED",
  physicalDevices: "NOT TESTED",
};
const assert = (v, text) => {
  if (!v) throw Error(text);
};
const password = randomBytes(24).toString("hex");
const htmlBytes = await fs.readFile(dir + "/RIGHTS_REVIEW.html");
const auth = "Basic " + Buffer.from("review:" + password).toString("base64");
const server = createServer((req, res) => {
  if (req.headers.authorization !== auth) {
    res.writeHead(401, {
      "WWW-Authenticate": 'Basic realm="Private review QA"',
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
  res.end(htmlBytes);
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const base = `http://127.0.0.1:${server.address().port}/review`;
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  httpCredentials: { username: "review", password },
  deviceScaleFactor: 1,
  acceptDownloads: true,
});
const page = await context.newPage();
page.on("pageerror", (e) => report.errors.push(e.message));
page.on("request", (r) => {
  if (/^https?:/.test(r.url()) && r.url() !== base)
    report.externalRequests.push(r.url());
});
try {
  await page.goto(base);
  await page.locator("[data-group]").nth(5).waitFor();
  assert(
    (await page.locator("article.card").count()) === 26,
    "Not26 visual records",
  );
  assert(
    (await page.locator("article.archive").count()) === 6,
    "Not6 era-inspired records",
  );
  assert(
    (await page.locator('[data-classification="NEEDS REVIEW"]').count()) === 26,
    "Rights classifications missing or falsely cleared",
  );
  assert(
    (await page.locator("#assessment").textContent()).includes(
      "26 NEEDS REVIEW",
    ),
    "Consolidated assessment missing",
  );
  assert(htmlBytes.length < 1000000, "Private review exceeds 1MB target");
  report.rows.push({
    check:
      "26 NEEDS REVIEW classifications / integrity PASS distinct from public BLOCKED / under 1MB",
    status: "PASS; no permission clearance inferred",
  });
  const images = await page.locator(".views img").evaluateAll((images) =>
    images.map((i) => ({
      complete: i.complete,
      width: i.naturalWidth,
      height: i.naturalHeight,
      sampling: getComputedStyle(i).imageRendering,
    })),
  );
  assert(
    images.length === 104 &&
      images.every(
        (i) =>
          i.complete &&
          i.width === 96 &&
          i.height === 112 &&
          i.sampling === "pixelated",
      ),
    "Wrong native crops/sampling",
  );
  assert(
    await page.locator("#approve").isDisabled(),
    "Default approval is enabled",
  );
  assert(
    (await page.locator("#summary").textContent()).startsWith("0/26"),
    "Not pending by default",
  );
  await fs.mkdir(".cache/review-final-qa", { recursive: true });
  await page.screenshot({ path: ".cache/review-final-qa/desktop.png" });
  const manifestDownload = page.waitForEvent("download");
  await page.locator("#download-manifest").click();
  const manifest = await manifestDownload;
  const manifestFile = ".cache/review-final-qa/exact-manifest.json";
  await manifest.saveAs(manifestFile);
  const hash = createHash("sha256")
    .update(await fs.readFile(manifestFile))
    .digest("hex");
  assert(
    hash === "40c129fb774adf14e2bd9f707d2c50e5fe24d89d438d654172ed02e33b73018d",
    "Downloaded manifest is not byte-exact",
  );
  const provenanceDownload = page.waitForEvent("download");
  await page.locator("#download-provenance").click();
  const provenance = await provenanceDownload;
  await provenance.saveAs(".cache/review-final-qa/provenance.json");
  const a = JSON.parse(
    await fs.readFile(".cache/review-final-qa/provenance.json", "utf8"),
  );
  assert(
    a.sourceEvidenceChecks === 309 &&
      a.rows.length === 26 &&
      a.commercialRelease === "BLOCKED_PENDING_REVIEW",
    "Wrong provenance download",
  );
  report.rows.push({
    check:
      "26records/104nativecrops/6era records/defaultpending/exactdownloads",
    status: "PASS",
    manifestSHA256: hash,
  });
  const first = page.locator("article.archive").first();
  await first.locator("select").selectOption("HOLD");
  const pendingDownload = page.waitForEvent("download");
  await page.locator("#pending").click();
  const pending = await pendingDownload;
  await pending.saveAs(".cache/review-final-qa/hold.json");
  const hold = JSON.parse(
    await fs.readFile(".cache/review-final-qa/hold.json", "utf8"),
  );
  assert(
    hold.decision === "PENDING" &&
      Object.values(hold.npcReviews).some(
        (r) => r.decision === "HOLD" && r.unresolvedSpecificConcern === true,
      ),
    "Hold became approval",
  );
  assert(
    await page.locator("#approve").isDisabled(),
    "Hold allowed public approval",
  );
  report.rows.push({ check: "HOLD cannot become approved", status: "PASS" });
  // Synthetic UI fixture only. No real receipt is edited or uploaded.
  await page.locator("#owner").fill("SYNTHETIC QA ONLY — NOT OWNER APPROVAL");
  await page.locator("#when").fill("2026-10-29T12:00");
  await page
    .locator("#reason")
    .fill("SYNTHETIC UI TEST ONLY. No public exposure permission granted.");
  for (const card of await page.locator("article.card").all()) {
    await card.locator("select").selectOption("ALLOW_PUBLIC_PREVIEW");
    await card.locator("[data-field=reviewed]").check();
    await card
      .locator("textarea")
      .fill(
        "SYNTHETIC FORM VALIDATION, NOT A DEPICTION FINDING OR OWNER DECISION",
      );
  }
  for (const group of await page.locator("[data-group]").all())
    await group.check();
  await page.locator("#ack").check();
  assert(
    await page.locator("#approve").isEnabled(),
    "Complete synthetic form cannot export",
  );
  const syntheticDownload = page.waitForEvent("download");
  await page.locator("#approve").click();
  const synthetic = await syntheticDownload;
  const fixture = ".cache/review-final-qa/SYNTHETIC-NOT-OWNER.json";
  await synthetic.saveAs(fixture);
  const result = JSON.parse(await fs.readFile(fixture, "utf8"));
  assert(
    result.decision === "APPROVED_PUBLIC_PREVIEW" &&
      result.approvedBy.startsWith("SYNTHETIC") &&
      Object.keys(result.npcReviews).length === 26 &&
      result.artifactCommit === "ee0a928735d5bed527f2a3ce100b615274224061",
    "Export contract broken",
  );
  await fs.unlink(fixture);
  await first.locator("[data-field=note]").fill("");
  assert(
    await page.locator("#approve").isDisabled(),
    "Era review missing note accepted",
  );
  report.rows.push({
    check: "complete synthetic export contract / missing-era-note rejection",
    status: "PASS synthetic UI only; fixture deleted; no real approval",
  });
  // Reload clears the form; do not leave even synthetic approval state in screenshots.
  for (const viewport of [
    { width: 390, height: 844 },
    { width: 667, height: 375 },
  ]) {
    await page.setViewportSize(viewport);
    await page.reload();
    await page.locator("[data-group]").nth(5).waitFor();
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      "Mobile overflow",
    );
    await page.locator("#zoom").check();
    const size = await page.locator(".views img").first().boundingBox();
    assert(
      size.width === 192 && size.height === 224,
      "Enlargement not integer2x",
    );
    await page.locator("#zoom").uncheck();
    await page.screenshot({
      path: `.cache/review-final-qa/mobile-${viewport.width}.png`,
    });
  }
  report.rows.push({
    check: "mobileportrait/landscape +native1x/integer2x preview",
    status: "PASS browser emulation",
  });
  assert(
    !report.errors.length && !report.externalRequests.length,
    "Standalone page uses network or crashes",
  );
  const real = JSON.parse(
    await fs.readFile(
      "/workspace/review-pages-destination/review-candidates/phase3b-a.json",
      "utf8",
    ),
  );
  assert(
    real.decision === "PENDING" &&
      Object.values(real.npcReviews).every((r) => r.decision === "PENDING"),
    "Real pending decision was changed",
  );
  report.status = "PASS LOCAL REVIEW PAGE; PUBLIC APPROVAL STILL PENDING";
} catch (e) {
  report.status = "FAIL";
  report.failure = e.stack;
  console.error(e);
  process.exitCode = 1;
} finally {
  await fs.writeFile(
    dir + "/VISUAL_PAGE_QA.json",
    JSON.stringify(report, null, 2) + "\n",
  );
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
