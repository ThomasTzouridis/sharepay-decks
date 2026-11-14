"""SharePay deck slug for NEW leads (rule since 2026-11-14): <company>-<first name>-<last name>.
   py tools/slug.py "Son-Vidéo.com" Hugo Lahutte   ->  son-video-com-hugo-lahutte
The same value goes into the HeyReach custom field `presentation` (https://sharepay-cases.com/<slug>/) when the lead is
uploaded, and into specs/<slug>.json. Decks and HeyReach fields made before 2026-11-14 keep their old /<company>/ slug.
"""
import re, sys, unicodedata

FOLD = str.maketrans({'ø': 'o', 'Ø': 'O', 'æ': 'ae', 'Æ': 'AE', 'ß': 'ss', 'ł': 'l', 'Ł': 'L', 'đ': 'd', 'Đ': 'D', 'þ': 'th', 'œ': 'oe', 'Œ': 'OE', '&': ' and '})


def slug(company, first='', last=''):
    s = ' '.join(x for x in (company, first, last) if x and x.strip())
    s = s.translate(FOLD)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

if __name__ == '__main__':
    assert len(sys.argv) >= 2, __doc__
    print(slug(*sys.argv[1:4]))
