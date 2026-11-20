# The World / One Day — 19 November 2026

An original, illustrated front page with eight English-language stories. The summit leads; four other major developments and three briefs round out the page. The custom illustration emphasizes the shared table and declaration, not an end to the wars. The smaller drawings show a verdict, a trading debut, deleted draft language, a shipping bottleneck, a one-day signal, an evacuation and a console launch.

## Run

`python main.py` uses Python 3.13's standard library. It copies the bundled PNG to `/output/entry.png` or to `entry.png` in the directory set by `MAKEFUN_OUTPUT_DIR`. Run `python test_entry.py` to check deterministic output in two separate directories with socket operations forbidden.

## Edit the page

`stories.json` contains the exact on-image text, attribution and a source URL for each story. `render.py` draws every illustration from shapes. Use Python 3.13 with Pillow 13.0.0: `uv run --no-project -p 3.13 --with pillow==13.0.0 python render.py`. Rendering needs installed Georgia, Segoe UI and Consolas fonts (set `DIGEST_FONT_DIR` if not using the Windows Fonts directory). No font files are bundled or needed by `main.py`.

## Editorial notes

- Voyager 1 reached the threshold on November 18; NASA received the signal and confirmed it November 19. The news is the confirmation.
- COP31 coverage refers to the revised November 19 draft, not an adopted agreement.
- The energy superlative is attributed to the IEA. The summit declaration did not establish a peace deal for Ukraine.
- The market report uses the reported closing gain; no IPO offer price is depicted.

Local artwork and source for review. This archive is not a make.fun submission or a transcript bundle.
