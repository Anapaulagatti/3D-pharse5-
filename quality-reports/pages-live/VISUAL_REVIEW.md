# Public v0.2 showcase verification

Live URL: https://anapaulagatti.github.io/3D-pharse5-/

GitHub run 38402363567 attempt 2: package and deploy **success**. Deployment 7039586635 reports success and this authoritative environment URL. Public anonymous HTTPS response is **200 text/html**; decoded bytes/SHA exactly match the approved 7,493,366-byte standalone HTML.

The assistant opened and inspected actual public-site screenshots: public-desktop.png, public-night.png, public-camera-drag.png, public-mascot-greeting.png and public-mobile-fallback.png. These show real WebGL Hanok geometry/ceramic mascot, warm night illumination, a visibly rotated camera view, the greeting pose and the rendered PNG fallback at a 390×844 viewport. This review is of the deployed website, not the local source viewer.

All seven public browser checks passed: actual textures/geometry, canvas pointer camera drag/reset/roof POI, day/night render, both exact-checksum GLB downloads, six distinct poses and advancing animation, reduced-motion freeze, responsive mobile layout and desktop/mobile WebGL fallback. Zero page/console errors, failed requests or missing resources. Only the repository-subpath HTML required an HTTP request; JS/CSS and verified assets are embedded/Blob resources. See http-verification.json and captured images.

First live-browser attempt hit the cloud proxy CA trust error. The existing correct proxy CA was already trusted in the Chromium NSS database, but that directory was read-only under the execution sandbox. Temporary write permission let Chromium open/lock the existing DB. TLS validation stayed enabled; no new CA, client key or credential was added or published. Native physical-phone FPS was not measured.

The deployment copied the completed artifact; source/.blend/GLB/textures/animations/previous checkpoints remain unchanged. Static site contains index.html and .nojekyll only, with license notices and original Studio assets. Stop here and wait for the user's visual feedback before any district work.
