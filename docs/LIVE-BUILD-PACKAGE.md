# Vultr Agent Rush — Live-Build Package (Nov 3–8, 2026)

**Prepared:** Wed Nov 4, 2026 (build window day 2 of Nov 3–8).
**For:** Umar Shareef — LabLab APPROVED, solo, online only.
**Project:** "Sandbox Ops Agent" in `~/workspace/vultr-agent-rush/`
**Status at preparation time: NOT deployed, NOT submitted, NOT paid.**
Nothing in this package deploys, pays, submits, or contacts anyone.
It is a plan + checklist + draft only.

## 0. What is already true (verified for this package)

- Project built Oct 28, 2026: Planner → Coder → SandboxExecutor → Verifier,
  allowlist containment, web UI in `public/index.html`, stdlib-only Python
  (`src/server.py`, `src/agents.py`) — no pip dependencies.
- Tests re-run for this package: **9/9 PASS** (`python3 -m unittest discover -s tests`).
- Local commit: `316e50b` "Sandbox Ops Agent: multi-agent mock Vultr sandbox demo".
  **No public repo push yet** (see §2).
- README already contains the required Vultr integration explanation, but it
  is written in future tense ("in the live build, the mock adapter is
  swapped…") — that wording stays honest until a live run is actually tested.
- LabLab email (Nov 3): build is LIVE Nov 3–8, 2026; claim **$200 free
  Vultr credits via the event page**; live Q&A was **Nov 3, 6:00 PM CET on
  Discord**; create/join a team even if solo.
  - ⚠️ The Nov 3 Q&A time has already passed by the time this package was
    written (Nov 4). Do NOT present it as upcoming. Whether a recording
    exists is unverified — check Discord/LabLab if needed, do not invent one.
- Hybrid finale Salt Lake City Nov 8: **Umar does NOT travel — online only.**
  This was his confirmed decision; do not change it.

## 1. Step-by-step live deployment plan (free $200 credits only)

**Hard rule for every step: if any screen asks for a card, a paid upgrade,
a paid add-on, or a payment method — STOP at that step. Do not enter a
card, do not pay, do not work around it. Report the exact screen to Umar
and wait for his explicit decision for that item.**

### Step A — Umar-only: claim the $200 credits (needs his LabLab login)
1. Umar signs in to LabLab (Muse cannot do this for him — LabLab login is his).
2. On the official LabLab/Vultr event page, claim the $200 participant
   credits exactly as the LabLab setup guide states.
3. Record: credit amount shown, expiry/conditions shown (do NOT assume an
   expiry — the LabLab email in hand states no expiry, and the old plan
   notes prize distribution may take up to 90 days, which is a different
   thing and must not be confused with credit expiry).
4. ⛔ STOP if the claim flow asks for a card. Free credits must not require one.

### Step B — Umar-only: Vultr account (if he does not already have one)
1. Create/sign in to Vultr with his own account (his email, his login).
2. Verify the $200 credit balance appears on the Vultr dashboard/billing page
   before provisioning anything.
3. ⛔ STOP if Vultr account creation or credit activation demands a card.

### Step C — Provision one small CPU instance (no GPU, no paid extras)
1. Region: pick any region shown on the dashboard (no region is prescribed
   by the material in hand — record the one actually chosen).
2. OS: a current Ubuntu LTS image (stdlib Python 3 is all the app needs).
3. Size: the **smallest instance whose listed price fits inside the $200
   credit balance** — read the price on the dashboard at provisioning time
   and write it down; do NOT quote a price from memory, prices change.
4. Decline every paid add-on: backups, snapshots, extra IPs, monitoring
   upgrades, GPU (per the project README, Vultr GPUs are not available for
   this event in any case — do not select one).
5. ⛔ STOP if the instance cannot be created without adding a payment method.

### Step D — Deploy the app (one code change is required — be honest about it)
Current code binds to `127.0.0.1` (`src/server.py`, `HTTPServer(("127.0.0.1", port), ...)`),
which is correct locally but unreachable from the internet. For the live build:
1. SSH into the instance (Umar's key / Vultr console — his credentials only).
2. Install only `python3` (and `git`). The app has **no pip dependencies**,
   so no requirements file or paid service is needed.
3. Clone the **public repo** (only after the §2 repo push — the live URL must
   serve the same commit that is pushed, or the submission is inconsistent).
4. Change the bind address to `0.0.0.0` (keep `PORT` from the environment,
   default 8001). Keep every containment check in `src/agents.py` unchanged
   — the live build swaps *where* code runs (on the Vultr VM), not the
   containment rules. Do NOT claim the VM alone makes execution safe; the
   allowlist/block rules are the containment, and they must still run.
5. Run it persistently (e.g. a systemd unit with `WorkingDirectory` set to
   the repo root, so `public/index.html` resolves — the server serves files
   relative to the working directory). Open only the app port in the Vultr
   firewall; close SSH to trusted sources where the dashboard allows it.
6. Health check from a browser: `http://<instance-IP>:<PORT>/api/health`
   must return `{"status": "ok", ...}`.

### Step E — Live test (this is what turns "mock" into "live" honestly)
1. Safe task on the LIVE URL: "Add up 12, 28 and 40" → verified output **80**.
2. Containment moment on the LIVE URL: "Show containment block" with
   `rm -rf /` → blocked, reason shown, nothing executed.
3. Re-run the full local suite: `python3 -m unittest discover -s tests` → 9/9.
4. Only after steps 1–3 pass on the live URL may the README/demo wording
   change from "mock Vultr sandbox mode" to live Vultr mode, and only for
   the exact behaviour actually tested. Until then the app must still be
   labelled mock mode (see `docs/DEMO-SCRIPT.md` checklist).
5. If any live test fails, fix, re-test, and re-record — do NOT submit a
   video recorded against the local mock and describe it as the live demo.

### Step F — After the event window
- Keep the instance running only while it is needed for judging/demo; the
  $200 credits are participant credits, not a commitment to keep paying.
- Before Nov 8 ends, capture the live URL, the tested commit, and the demo
  video link in the submission — then do NOT change repo/video/links after
  the lock (per the original plan).

## 2. Submission checklist — done vs missing

| Item | Status | Evidence / next action |
|---|---|---|
| LabLab approval | ✅ DONE | Email Oct 28, 2026; build window Nov 3–8 confirmed live by Nov 3 email |
| Solo, online-only decision | ✅ DONE | Confirmed; NO Salt Lake City travel Nov 8 |
| Project built (mock mode) | ✅ DONE | `src/`, `public/`, tests 9/9 re-verified for this package |
| README Vultr integration explanation | ✅ DONE (future tense) | Update to past tense only after §1 Step E passes |
| Demo video script | ✅ DONE | `docs/DEMO-SCRIPT.md` (2:45 target, ≤3:00, containment moment required) |
| Local commit | ✅ DONE | `316e50b`, clean working tree at preparation time |
| Discord connect | ❌ MISSING — Umar only | LabLab profile → Connect Discord → authorize → join server. Not done by Muse, not invented. Draft intro in §3, NOT sent |
| Online attendance confirmation | ❌ MISSING — Umar only | LabLab confirmation form → select ONLINE (not onsite) → submit. Unconfirmed in every record to date |
| Team create/join (LabLab email says "even if solo") | ❌ UNRESOLVED — needs a decision | LabLab email says create/join a team even if solo; the original plan says confirm solo entry and do NOT join a team without approval. Resolve on the LabLab dashboard as a **solo team/entry**; do NOT join another person's team without Umar's explicit approval |
| $200 credits claim | ❌ MISSING — Umar only | Via official LabLab/Vultr event page; ⛔ STOP on any card request |
| Public repo push | ❌ MISSING | Push commit `316e50b` (plus the §1 Step D bind change, as a new commit) to a public repo under `umarshareef0165-netizen`; record the exact repo URL |
| Live Vultr URL | ❌ MISSING | Only after §1 Steps C–E; record IP/URL and the exact tested commit |
| Live test (safe task + containment) | ❌ MISSING | Must be run on the live URL, not localhost, before any "live" claim |
| Demo video recorded (user-recorded screen capture) | ❌ MISSING | Record per `docs/DEMO-SCRIPT.md` from the LIVE URL; public video, ≤3:00, no credential visible in any frame; never a generated video |
| LabLab submission | ❌ MISSING — needs Umar's final approval | Exact LabLab submission fields are NOT in the material in hand — verify them on the LabLab submission form at submit time (expected, not guaranteed: repo URL, live demo URL, demo video link, project description, Vultr integration explanation, agent use case + how it executes real tasks, containment moment). Submit only after his separate final approval |

**Prizes (from the original plan, re-check on LabLab before quoting):**
1st $5,000 + $3,000 credits; 2nd $3,000 + $1,000 credits;
3rd $1,000 + $1,000 credits; every participant $200 credits.
Prize distribution may take up to 90 days. **Winning is not guaranteed.**

## 3. Discord intro draft — DO NOT SEND (Umar's step, after he connects Discord)

> Hi everyone — I'm Umar Shareef, solo and joining online only for the
> Vultr Agent Rush. I'm building "Sandbox Ops Agent": a multi-agent
> system (Planner → Coder → Sandbox → Verifier) that does real ops/support
> tasks but can never escape its sandbox — every unsafe action is blocked
> and shown as a visible containment moment. It's stdlib Python, CPU-only,
> and I'm deploying it live on Vultr with the participant credits for the
> Nov 3–8 build. Happy to take feedback on the containment design and the
> live demo — and good luck to all builders here!

Notes on the draft: it states only verified facts (solo, online, project
name, architecture, CPU-only, credits-funded live deployment as a plan).
It does NOT claim a live URL, a repo push, or a Vultr deployment that does
not exist yet. Edit the last line once the live URL exists; do not post a
version that claims it early.

---
*Prepared as a plan only. No deployment, payment, submission, Discord join,
or contact was made in preparing this file.*
