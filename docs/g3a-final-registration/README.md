# Final G3-A world-registration approval review

The user provisionally accepts the rendering corrections as a technical fix. The corrected renderer is preserved at commit **15ebbfd**, with the verified playable archive at **2934683**. Both existing checkpoint tags remain unchanged:

- `checkpoint/g3a-pixel-fidelity-review-20261023`
- `checkpoint/g3a-pixel-fidelity-package-20261023`

**[Final building-registration proposal](PROPOSAL.md)** · [Native visual review page](index.html) · [Preservation proof](preservation-proof.json)

## Direct native 1:1 evidence

These links open the original, unmodified1280×900 PNGs. View/download at100% zoom; fit-to-window previews may rescale them. The [review page](index.html) supplies scrollable native-size images without enlargement or fit-to-width scaling.

| Scene / renderer | Before | After |
|---|---|---|
| Station frontage / Canvas correction | [Native PNG](../gate3a-pixel-audit/before-canvas-native.png) | [Native PNG](../gate3a-pixel-audit/after-canvas-native-backing.png) |
| Station frontage / WebGL control | [Native PNG](../gate3a-pixel-audit/before-auto-native.png) | [Native PNG](../gate3a-pixel-audit/after-auto-native-backing.png) |
| Stationary gameplay / WebGL | [Native PNG](../gate3a-pixel-audit/before-auto-stationary.png) | [Native PNG](../gate3a-pixel-audit/after-auto-stationary-backing.png) |
| Moving-camera gameplay / Canvas | [Native PNG](../gate3a-pixel-audit/before-canvas-moving.png) | [Native PNG](../gate3a-pixel-audit/after-canvas-moving-backing.png) |

Canvas image-destination expansion was removed: **2,943 → 0** mismatches over1,108,756 unobstructed ground pixels; both complete planter boxes now match their source composite. The odd-window canvas origin changed from `(0.5,50.5)` to `(0,50)` CSS pixels. Integer native placement and nearest sampling remain enforced. The station's0.5px pivot resolves to integer raster placement and was not the blur cause.

WebGL already reproduced the approved source exactly in the native view. **No WebGL source-detail improvement is claimed.** Remaining painted/previously resized source softness is visible in the approved PNGs and is documented [separately from renderer defects](../gate3a-pixel-audit/REPORT.md). Nothing was sharpened, upscaled, recolored, regenerated or relocated for this handoff.

## Playable package and unresolved evidence

The [existing corrected playable ZIP](../gate3a-pixel-audit/G3A_PIXEL_CRISP_REVIEW.zip) remains unchanged,91,801,078 bytes, SHA256 `bc273c7f83a6b01622523bcd529a83f93b503ab8ff60d7f9d3f9b2e8def5d81a`. It contains the candidate registration scene, preserved district and world foundation. Extract, run `python3 -m http.server 4281 --bind 127.0.0.1`, open `http://127.0.0.1:4281/`. No public deployment.

- WebGL performance remains **UNRESOLVED**. Existing SwiftShader diagnostics do not certify hardware/mobile GPU performance; culling reduced work without proving an FPS gain.
- Physical Android Chrome and iPhone Safari remain **NOT TESTED**. Keep the [existing device checklist and export workflow](../gate3a-corrections/DEVICE_CHECKLIST.md); emulation/exported JSON alone is not device acceptance.
- Registration and localized planning amendments remain **PENDING HUMAN APPROVAL**. Read the proposal's conflict table before approving, especially the bakery/carousel projection, five bakery path amendments, retail visual easements and station/platform composition.
- G3-B mass artwork remains **BLOCKED**. No masterplan change, protected checkpoint modification, merge or deployment occurred.

**Please approve or request changes to the final individual-building world-registration proposal. Technical rendering acceptance does not authorize G3-B.**
