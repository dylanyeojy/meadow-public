# Assets

Fonts are documented in [fonts/README.md](fonts/README.md).

## Icons (`icons/`)

Extracted from Meadow's Claude Design project, so they match the mockups exactly. The design draws its own icons rather than using a published set.

Each file draws in `currentColor` with no colour of its own, and the app tints every icon from its palette at runtime, so the one-palette rule holds for icons too. Each file keeps the stroke width the design used for it.

`eye.svg` is the one icon not in the design: the mockups only draw the closed eye on password fields. It is drawn to match `eye_off.svg`.

Two shapes in the design were skipped: the sample line chart on Home and Stats, which is a chart rather than an icon, and a duplicate of `notice.svg` written with a different but identical path.
