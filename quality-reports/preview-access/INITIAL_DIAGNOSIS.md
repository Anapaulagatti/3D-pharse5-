# Initial HTTP preview diagnosis

The source viewer in ChatGPT/Codex is not an HTTP host. The actual Vite server returned HTTP 200 with Content-Type text/html and rendered the application. No user-facing browser preview/port-forwarding tool is exposed in this onboarding environment.

The first current-run development smoke test exceeded its five-second ready assertion on the cloud software GPU. Eight other tests passed; an attempted first-test retry also exceeded five seconds. The same production scene subsequently reached ready in 3,603 ms and camera/day/night/six-pose/render checks completed. The smoke readiness allowance was changed to 15 seconds for cold software shader compilation, keeping the same ready-state and rendering assertions. The fresh full rerun is recorded separately.

Initial production HTTP console check found one 404: http://127.0.0.1:4173/favicon.ico. Chromium CDP and the console message location confirmed this request. Both GLBs, application JavaScript and CSS returned 200; approved export checksums passed. Added an inline empty favicon declaration to the preview HTML and standalone HTML generator to avoid the default favicon request. No 3D content, material, model, animation or art direction changed.

GitHub native Git read/push is available. GitHub Pages API read returned Forbidden, and unauthenticated raw HTML fetch returned 404; neither is a working website preview. A manual-only Pages workflow and static upload package are prepared, with no public deployment performed.
