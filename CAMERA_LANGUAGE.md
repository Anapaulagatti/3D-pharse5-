# Camera language

- Default: orthographic 3/4 view toward courtyard center; front-facing mascot is visible from positive world Z. Blender source uses Z-up, exported glTF uses Y-up; 1 unit equals roughly 1 meter.
- Desktop composition: whole collectible plinth, pavilion, gateway and skyline visible with breathing space; leave foreground around central mascot readable.
- Phone composition: widen camera fit from measured viewport width, keep important objects inside frame; use a slightly higher target, never crop the primary mascot.
- Orbit is bounded above the courtyard, with no pan through architecture. Reset returns to the initial framing. Focus points shift target gently unless reduced motion is enabled.
- Introduction: a short damped settling movement, no continuous camera spin. Reduced motion uses the final framing immediately.
- Character showcase: zoomed view on a small ceramic display base, isolated from architecture; same materials and lighting palette as arena.
- Static posters derive from actual render output of the saved models, not the AI concept sheet.
