/** Captured analog stick: independent pointer, radial deadzone, no synthetic key presses. */
export function attachJoystick(
  el: HTMLElement,
  vector: (x: number, y: number) => void,
  blocked: () => boolean,
) {
  const knob = el.querySelector<HTMLElement>(".stick-knob")!;
  let pointer: number | undefined;
  const reset = () => {
    pointer = undefined;
    knob.style.transform = "translate(0px,0px)";
    el.dataset.active = "false";
    vector(0, 0);
  };
  const move = (e: PointerEvent) => {
    const b = el.getBoundingClientRect(),
      r = b.width * 0.34,
      dx = e.clientX - b.x - b.width / 2,
      dy = e.clientY - b.y - b.height / 2;
    const length = Math.hypot(dx, dy),
      distance = Math.min(r, length),
      unit = length ? 1 / length : 0;
    const strength = Math.max(0, (distance / r - 0.14) / 0.86);
    knob.style.transform = `translate(${dx * unit * distance}px,${dy * unit * distance}px)`;
    vector(dx * unit * strength, dy * unit * strength);
  };
  el.onpointerdown = (e) => {
    e.preventDefault();
    if (blocked() || pointer !== undefined) return;
    pointer = e.pointerId;
    el.setPointerCapture(pointer);
    el.dataset.active = "true";
    move(e);
  };
  el.onpointermove = (e) => {
    if (e.pointerId === pointer) {
      e.preventDefault();
      if (blocked()) reset();
      else move(e);
    }
  };
  const release = (e: PointerEvent) => {
    if (e.pointerId === pointer) reset();
  };
  el.onpointerup = release;
  el.onpointercancel = release;
  el.onlostpointercapture = release;
  return reset;
}
