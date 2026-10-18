# Capture/encoding diagnostics retained

The normal-entry public-touch walkthrough completed all13route segments with0page/console/resource errors. Both simultaneous streams are original observations, not synthesized animation frames.

Initial strict encoder attempt rejected12out-of-order CDP delivery events. All9282unique capture timestamps remain unchanged in capture.json; encoding orders the entire original set by capture timestamp, preserving every frame. No discards or invented timestamps.

Next attempt preserved9282frames but independently measured0.0050971355s maximum accumulated PTS drift from rounding each ffconcat duration. Kept the <=0.002s gate; fixed input construction by quantizing absolute original timestamps to1ms first, then subtracting adjacent absolute ticks. All quantized ticks are strictly increasing. No FPS filter/interpolation/duplication.

Original MediaRecorder VP9 WebM lacks container duration metadata. Verification initially raised KeyError:duration. The original file is retained unchanged, and native average capture FPS is instead computed from decoded frame count and measured first/last presentation timestamps. This is separate from CDP delivery/MP4 and actual Phaser runtime FPS. Final independently decoded report is video-verification.json; real browser playback report is video-playback.json.

Full-browser source JPEG files stay only in ignored .cache/living-korea/tour-* because they total over1GB. Every original timestamp/byte count/SHA is checkpointed in capture.json; original VP9 and timestamp-preserving H264 review are checkpointed. Execution caches are not promised to survive environment restoration.

Browser harness initially reported a directory-server favicon404, then exposed that Python SimpleHTTPServer does not support media Range seeking: MP4 seeks silently stayed at0. Stale headless video-layer screenshots therefore could not serve as evidence. Kept strict decoded-time/pixel checks, served harness favicon204 and fetched the complete original media over HTTP into a Blob before playback/seek. Each requested seek must now reach its actual time within0.1s. Decoded-video canvas pixels must differ during2.2snormal playback. Final corrected browser-decoded PNGs replace only those failed harness captures (distinct PNG hashes checked and contact sheet visually inspected); no game or video frames were changed. Final video-playback.json has0errors.
