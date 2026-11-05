# Sandbox Ops Agent — Vultr Agent Rush (LabLab)

**Hook:** an agent that does real work — but can never escape its sandbox.
A user task is planned, coded, run inside a contained sandbox, and verified
before any result is reported. Every unsafe action is blocked and logged as a
visible containment moment.

## Status
- Solo, online only. Umar Shareef is APPROVED by LabLab (email 2026-10-28).
- Build window: **Nov 3–8, 2026**. Hybrid finale Salt Lake City Nov 8 — the
  author will **NOT travel**; online participation only.
- Current build: **mock Vultr sandbox mode**. No real Vultr API key, LLM key,
  or credential exists or is claimed. Nothing submitted, nothing paid.

## How it maps to the challenge (from lablab.ai / Vultr community pages)
- Web-based agent that writes and runs code, with every action contained
  inside a sandbox — here modelled by `src/agents.py:SandboxExecutor`, to be
  replaced by a real Vultr VM/container adapter with the same interface.
- Multi-step workflow: Planner → Coder → SandboxExecutor → Verifier.
- Containment first: allowlisted operations only; destructive deletes,
  network access, path traversal, system paths, remote access, and dynamic
  execution outside the sandbox are blocked before execution.
- Judging criteria addressed: Application of Technology (multi-agent +
  sandbox), Presentation (live web UI + demo video), Business Value
  (safe automation for ops/support tasks), Originality (containment shown,
  not just claimed).

## Vultr integration explanation (required in README)
In the live build, the mock adapter is swapped for a Vultr deployment:
a Vultr VM/container becomes the system of record for planning, coordination
and execution; the web app runs there, agent code runs only inside the
sandboxed execution environment, and results return through the same
verified API. The $200 participant credits (if granted) would fund that VM;
no credit, key, or deployment is claimed until it is actually provisioned.
Vultr GPUs are not available for this event, so the design uses CPU-only
demo workloads.

## Run it
```bash
cd ~/workspace/vultr-agent-rush
python3 src/server.py
# http://localhost:8001/  — try a safe task, then "Show containment block"
python3 -m unittest discover -s tests   # 9 tests
```

## Demo tasks that work in mock mode
- "Add up 12, 28 and 40" → 80
- "Sort 5, 2, 9, 1" → [1, 2, 5, 9]
- "Find the average of 10, 20, 30" → 20.0
- Containment demo: `rm -rf /` → blocked, "destructive delete", nothing runs

## What remains (see docs/PLAN.md)
LabLab Discord intro, solo confirmation, live Vultr deployment, live test,
demo video with at least one containment moment, LabLab submission approval.
