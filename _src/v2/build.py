"""SharePay deck v2 (personalized, 5 slides, 2026-11-03): py _src/v2/build.py _src/v2/specs/<slug>.json -> <slug>/index.html
The batch engine (_src/build.py, 4 slides, 164 decks of 2026-10-31) stays as it is; v2 is for hand-built decks with lead-specific slide 2 copy.

Spec fields (JSON):
  slug          folder name and URL part (required), = HeyReach custom field `presentation` slug (sharepay-cases.com/<slug>/)
  company       lead company, as it should read in text (required)
  first_name    first name of the lead
  last_name     last name of the lead (cover: "Prepared for <first_name> <last_name>, <company>")
  domain        the lead's site, shown under the screenshot (required)
  shot          file in assets/shots/ (required; take it with _src/tools/shot.py)
  logo          file in assets/leadlogos/, ALWAYS produced by tools/logo.py (py tools/logo.py <slug> "<Company>" https://<domain> --bg #0b1220 --out assets/leadlogos --spec specs/<slug>.json --badge-key logo_badge).
                No usable logo = key omitted = company name in text. build.py refuses a png that fails the guard.
  logo_badge    true = logo on a white badge (for dark logos)
  sender_first  first name of the SharePay sender (default Safwaan)
  cover_line    optional, default "Fewer checkout drop-offs at <domain>. No setup fee, no retainer, 3% of what we bring in."
  saw_head      slide 2 headline (lead specific)
  saw_l1, saw_l2, saw_turn   slide 2 lines (lead specific; saw_turn sits in the green bar)
  measure       slide 3 step 02 text (optional, default below)
  talk_text     optional sentence under the Let's talk headline
  talk_img      file in assets/img/ for the closing picture (default experiences.jpg)
  booking_url   optional, default the SharePay cal.com discovery call
"""
import json, sys, os, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
BG = '#0b1220'   # the deck --paper, the logo tool checks against it
BOOK = 'https://cal.com/sharepay/discovery-call'
for path in sys.argv[1:]:
    sp = json.load(open(path, encoding='utf-8'))
    e = html.escape
    co = e(sp['company'])
    for k in ('slug', 'company', 'domain', 'shot', 'saw_head', 'saw_l1', 'saw_l2', 'saw_turn'):
        assert sp.get(k), f'{path}: missing {k}'
    assert os.path.exists(os.path.join(ROOT, 'assets', 'shots', sp['shot'])), f'{path}: shot file missing'
    name = ' '.join(x for x in (sp.get('first_name', '').strip(), sp.get('last_name', '').strip()) if x)
    prep = f"{e(name)}, {co}" if name else co
    mark = f'<span class="co">{co}</span>'
    if sp.get('logo'):
        lp = os.path.join(ROOT, 'assets', 'leadlogos', sp['logo'])
        assert os.path.exists(lp), f'{path}: logo file missing'
        sys.path.insert(0, os.path.join(ROOT, '_src', 'tools')); from logo import guard
        bad = guard(lp, BG, sp.get('logo_badge'))
        assert not bad, f"{path}: logo {sp['logo']} is {bad}. Run: py tools/logo.py {sp['slug']} \"{sp['company']}\" https://{sp['domain']} --bg {BG} --out assets/leadlogos --spec {path} --badge-key logo_badge"
        fb = "var s=document.createElement('span');s.className='co';s.textContent=this.alt;(this.closest('.llb')||this).replaceWith(s)"
        img = f'<img class="ll" src="../assets/leadlogos/{sp["logo"]}" alt="{co}" onerror="{fb}">'
        mark = f'<span class="llb">{img}</span>' if sp.get('logo_badge') else img
    sender = e(sp.get('sender_first') or 'Safwaan')
    out = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    for k, v in {'COMPANY': co, 'PREPARED': prep, 'CO_MARK': mark, 'DOMAIN': e(sp['domain']), 'SHOT': sp['shot'],
                 'COVER_LINE': e(sp.get('cover_line') or f"Fewer checkout drop-offs at {sp['domain']}. No setup fee, no retainer, 3% of what we bring in."),
                 'SAW_HEAD': e(sp['saw_head']), 'SAW_L1': e(sp['saw_l1']), 'SAW_L2': e(sp['saw_l2']), 'SAW_TURN': e(sp['saw_turn']),
                 'MEASURE': e(sp.get('measure') or f"Checkout drop-off at {sp['company']} before and after, read from your own Stripe or Adyen reports, not from us. Every order that completes through Split or Forward is one that would have ended as a visitor leaving. Superdry's number landed in under 90 days."),
                 'TALK_TEXT': e(sp.get('talk_text') or f"Twenty minutes with {sp.get('sender_first') or 'Safwaan'}: where {sp['company']} loses buyers at the checkout today, the test-mode setup, and what the first 90 days look like."),
                 'TALK_IMG': sp.get('talk_img') or 'experiences.jpg', 'SENDER_FIRST': sender,
                 'BOOKING_URL': sp.get('booking_url') or BOOK}.items():
        out = out.replace('{{' + k + '}}', v)
    assert '{{' not in out, path
    d = os.path.join(ROOT, sp['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    print('built', sp['slug'])
