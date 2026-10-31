"""Build one SharePay deck per spec: py build.py specs/<slug>.json -> ../<slug>/index.html

Same engine and the same 4 slides as the VistaMails decks (Presentations/Vistamails/_src), SharePay copy and colours.

Spec fields (JSON):
  slug          folder name and URL part (required). It is the slug HeyReach already sends in the `presentation` field,
                https://sharepay-cases.com/<slug>/, so it is never invented here.
  company       lead company, as it should read in text (required; the HeyReach `normalizedcompanyname`, same as message 2)
  first_name    first name of the lead
  last_name     last name of the lead (cover: "Prepared for <first_name> <last_name>, <company>")
  domain        the lead's site, shown under the screenshot (required)
  shot          file in assets/shots/ (required, the cover shows it; take it with tools/shot.py <slug> ../assets/shots https://<domain>)
  logo          file in assets/leadlogos/, ALWAYS produced by tools/logo.py (py tools/logo.py <slug> "<Company>" https://<domain> --bg #0b1220 --out ../assets/leadlogos --spec specs/<slug>.json --badge-key logo_badge):
                it picks the site's wordmark, rejects icons, photos and pixel-small rasters, paints one-colour logos white, puts dark
                multi-colour logos on a white badge (logo_badge) and writes a preview on the deck background to assets/leadlogos/_preview/.
                No usable logo = key omitted = company name in text. build.py refuses a png that is small, square or dark without a badge.
  logo_badge    true = logo on a white badge (for dark logos)
  cover_line    optional, default "Fewer checkout drop-offs for <company>, from the shoppers you already have."
  proof_head    optional, default "What it did for others."
  booking_url   optional, default the SharePay Cal.com discovery call (Zeejah)
  (slide 2 is fixed: heading "How we work" + the offer from message 1, Superdry 23% in under 90 days, 3% of new business only,
   no setup fee or retainer; the company name is the only lead-specific part)
"""
import json, sys, os, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BG = '#0b1220'   # the deck --paper, the logo tool checks against it
BOOK = 'https://cal.com/sharepay/discovery-call'
LOGOS = ''.join(f'<img src="../assets/clients/{n}" alt="">' for n in
                ["stripe.png", "adyen.png", "worldpay.png", "visa.png", "mastercard.png", "amex.png"])
O_HEAD = ("We put SharePay Split on {co}'s checkout. A shopper who wants the order but cannot pay all of it right then forwards the "
          "checkout to someone who can, or splits it with their group, each on their own card. The same system cut Superdry's "
          "checkout drop-offs by 23% in under 90 days.")
O_TARGET = ("Fewer checkout drop-offs for {co}. Orders that would have died at the payment step complete instead, fully funded, "
            "in {co}'s own Stripe or Adyen account.")
O_COND = ("3% of the new business it brings in, nothing else. No setup fee, no retainer, no monthly fee, and no charge when a "
          "split does not complete.")
O_MISS = ("{co} pays nothing. No minimum, no contract term, and no bill for a month in which nothing completes.")
for path in sys.argv[1:]:
    sp = json.load(open(path, encoding='utf-8'))
    e = html.escape
    co = e(sp['company'])
    for k in ('slug', 'company', 'domain', 'shot'):
        assert sp.get(k), f'{path}: missing {k}'
    assert os.path.exists(os.path.join(ROOT, 'assets', 'shots', sp['shot'])), f'{path}: shot file missing'
    name = ' '.join(x for x in (sp.get('first_name', '').strip(), sp.get('last_name', '').strip()) if x)
    prep = f"{e(name)}, {co}" if name else co
    mark = f'<span class="co">{co}</span>'
    if sp.get('logo'):
        lp = os.path.join(ROOT, 'assets', 'leadlogos', sp['logo'])
        assert os.path.exists(lp), f'{path}: logo file missing'
        sys.path.insert(0, os.path.join(HERE, 'tools')); from logo import guard
        bad = guard(lp, BG, sp.get('logo_badge'))
        assert not bad, f"{path}: logo {sp['logo']} is {bad}. Run: py tools/logo.py {sp['slug']} \"{sp['company']}\" https://{sp['domain']} --bg {BG} --out ../assets/leadlogos --spec {path} --badge-key logo_badge"

        fb = "var s=document.createElement('span');s.className='co';s.textContent=this.alt;(this.closest('.llb')||this).replaceWith(s)"
        img = f'<img class="ll" src="../assets/leadlogos/{sp["logo"]}" alt="{co}" onerror="{fb}">'
        mark = f'<span class="llb">{img}</span>' if sp.get('logo_badge') else img
    out = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    for k, v in {'COMPANY': co, 'PREPARED': prep, 'CO_MARK': mark, 'DOMAIN': e(sp['domain']), 'SHOT': sp['shot'],
                 'COVER_LINE': e(sp.get('cover_line') or f"Fewer checkout drop-offs for {sp['company']}, from the shoppers you already have."),
                 'PROOF_HEAD': e(sp.get('proof_head') or "What it did for others."),
                 'O_HEAD': O_HEAD.format(co=co), 'O_TARGET': O_TARGET.format(co=co), 'O_COND': O_COND.format(co=co), 'O_MISS': O_MISS.format(co=co),
                 'LOGOS': LOGOS, 'BOOKING_URL': sp.get('booking_url') or BOOK}.items():
        out = out.replace('{{' + k + '}}', v)
    assert '{{' not in out, path
    d = os.path.join(ROOT, sp['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    print('built', sp['slug'])
