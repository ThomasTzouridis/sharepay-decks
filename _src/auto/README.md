# SharePay decks: the automatic per-lead pipeline (live 2026-11-14, hub server)

Hub job `sharepay_decks` (AIOS `automations/mac-hub/jobs/sharepay_decks.py`, every 30 min) runs `~/sp-decks/_src/auto/sp_poll.py`
on automation-hub-01. Port of the VistaMails poller (`Presentations/Vistamails/_src/auto/vm_poll.py`).

Every run, for every live HeyReach campaign `SharePay | <Sender>` (workspace key `HEYREACH_SHAREPAY_API_KEY`):
1. Slug rule (Thomas 2026-11-14): every lead not messaged yet carries `presentation = https://sharepay-cases.com/<company>-<first>-<last>/`
   (`_src/tools/slug.py`). Missing or old values are rewritten with PATCH UpdateLeadCustomFields on the campaign lead (HeyReach updates the
   list lead too). Leads already messaged keep the link they were sent.
2. Every connected lead gets its deck built at the slug in its field (batch engine `_src/build.py` + `template.html`, screenshot, logo via
   `tools/logo.py`), pushed, live at `https://sharepay-cases.com/<slug>/` before message 2 (connect + 3 h + 4 days). Max 40 per run.
3. Control check: the link HeyReach sends must end in the lead's slug and answer 200. Failures and leads without a website go to Slack.

Files: `sp_poll_state.json` (build status per slug), `sp_leads.json` (lead map), `sp_poll.lock`, logs in `runs/` (ignored).

    python3 _src/auto/sp_poll.py --dry      shows what would change, changes nothing
    python3 _src/auto/sp_poll.py            real run
    python3 _src/auto/sp_poll.py --slug x   build one slug
