# SharePay decks

Hosting (2026-10-22): repo `ThomasTzouridis/sharepay-decks` (this folder), GitHub Pages on `main`, domain `sharepay-cases.com` bought on Spaceship account ACTISCALE (auto-renew on, Spaceship basic DNS: 4 GitHub A records + `www` CNAME to thomastzouridis.github.io). Deck URL: `https://sharepay-cases.com/<slug>/`. Push = live in about a minute.

Slug per lead = HeyReach custom field `presentation` on the SharePay lists (workspace 169465), derived from `normalizedcompanyname`. `404.html` is served for every slug without a folder.

## Building a deck (since 2026-10-31)
Same engine as the Vistamails decks, SharePay copy and colours. From `_src`:
1. `py tools/shot.py <slug> ../assets/shots https://<domain>` (cover screenshot, file `<slug>_1.jpg`; rename to the spec's `shot`)
2. `py tools/logo.py <slug> "<Company>" https://<domain> --bg #0b1220 --out ../assets/leadlogos --preview ../assets/leadlogos/_preview --spec specs/<slug>.json --badge-key logo_badge --on-none remove` (the only way a lead logo gets in)
3. `py build.py specs/<slug>.json` -> `../<slug>/index.html`
Spec fields are documented at the top of `_src/build.py`. Slide 2 copy, the proof numbers and the partner marquee are fixed in `build.py` and `template.html`; only the lead slots change. Client context in `_private/CONTEXT.md` (never online).

## v2: hand-built personalized decks (since 2026-11-03)
For leads who replied, a 5-slide deck with lead-specific slide 2 copy (Cover, What we saw, How we work, Our work, Let's talk). Engine `_src/v2/` (`template.html`, `build.py`, `specs/<slug>.json`), the batch engine above stays untouched. Build from the repo root: `py _src/v2/build.py _src/v2/specs/<slug>.json` -> `<slug>/index.html`. Required spec fields on top of the batch ones: `saw_head`, `saw_l1`, `saw_l2`, `saw_turn` (slide 2); optional `cover_line`, `measure`, `talk_text`, `talk_img`, `sender_first`, `booking_url`. First deck: `akis-petretzikis` (Diana Alexaki, replied to Safwaan 2026-11-02), screenshot retaken without the cookie popup.
