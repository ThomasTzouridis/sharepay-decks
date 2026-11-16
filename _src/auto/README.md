# SharePay decks: the automatic per-lead pipeline (live 2026-11-14, hub server)

Hub job `sharepay_decks` (AIOS `automations/mac-hub/jobs/sharepay_decks.py`, every 30 min) runs `~/sp-decks/_src/auto/sp_poll.py`
on automation-hub-01. Port of the VistaMails poller (`Presentations/Vistamails/_src/auto/vm_poll.py`).

Every run, for every live HeyReach campaign `SharePay | <Sender>` (workspace key `HEYREACH_SHAREPAY_API_KEY`):
1. Slug rule (Thomas 2026-11-14): every lead not messaged yet carries `presentation = https://sharepay-cases.com/<company>-<first>-<last>/`
   (`_src/tools/slug.py`). Missing or old values are rewritten with PATCH UpdateLeadCustomFields on the campaign lead (HeyReach updates the
   list lead too). Leads already messaged keep the link they were sent.
2. Every connected lead gets its deck built at the slug in its field (batch engine `_src/build.py` + `template.html`, screenshot, logo via
   `tools/logo.py`), pushed, live at `https://sharepay-cases.com/<slug>/` before message 2 (connect + 3 h + 4 days). Max 40 per run.
3. Control check: the link HeyReach sends must end in the lead's slug and answer 200. Failures go to Slack.

Copy variants (Thomas 2026-11-16): campaigns named `SharePay | <Sender> (Operators)` build with spec `"copy": "split"` (split the bill only),
campaigns named `SharePay | <Sender>` (e-commerce) build with the original forwarding copy. Texts live in `_src/build.py` (O_HEADS, P_SUPERDRY, P_ASDA).

Files: `sp_poll_state.json` (build status per slug), `sp_leads.json` (lead map), `sp_poll.lock`, logs in `runs/` (ignored).

    python3 _src/auto/sp_poll.py --dry      shows what would change, changes nothing
    python3 _src/auto/sp_poll.py            real run
    python3 _src/auto/sp_poll.py --slug x   build one slug

**No website (Thomas 2026-11-16).** A lead without a website, or whose site gives no screenshot after 3 tries, gets the exact same deck without the website picture and without a logo lookup (company name as text). The spec then has no `domain` and no `shot`. No lead stays on the fallback page for that reason.
