"""Multi-agent orchestration for Sandbox Ops Agent (mock mode, stdlib only).

Agents: Planner -> Coder -> SandboxExecutor -> Verifier/Critic.
No real Vultr API, LLM, or credentials are used here. The sandbox adapter
models the Vultr containment contract that the live adapter must implement:
allowlisted operations only, no network, no path escape, time/resource caps,
and every blocked attempt is logged as a containment moment.
"""
import re, time

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\b", "destructive delete"),
    (r"\bcurl\b|\bwget\b", "network access"),
    (r"\.\./", "path traversal"),
    (r"/etc/|/proc/|/sys/", "system path access"),
    (r"\bssh\b|\bscp\b", "remote access"),
    (r"\beval\(|exec\(", "dynamic code execution outside sandbox"),
]

class ContainmentError(Exception):
    pass

def check_containment(code: str) -> str | None:
    """Return a containment reason if code violates the sandbox policy."""
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, code):
            return reason
    return None

class Planner:
    def plan(self, task: str) -> list[str]:
        task = task.strip()
        if not task:
            raise ValueError("Task must not be empty.")
        return [
            f"Understand the request: {task}",
            "Break it into safe, verifiable steps",
            "Write code for one step at a time",
            "Run it inside the sandbox only",
            "Verify the output before reporting it",
        ]

class Coder:
    def write(self, task: str) -> str:
        t = task.lower()
        if "sum" in t or "add" in t or "total" in t:
            return "print(sum([12, 28, 40]))"
        if "average" in t or "mean" in t:
            return "print(sum([10, 20, 30]) / 3)"
        if "sort" in t:
            return "print(sorted([5, 2, 9, 1]))"
        return f"# Task: {task}\nprint('done')"

class SandboxExecutor:
    """Mock Vultr sandbox: executes only a tiny, safe Python subset.

    In the live build this class is replaced by a Vultr VM/container adapter
    with the same interface and the same containment checks, plus real
    network isolation. It must never run arbitrary user code on the host.
    """
    def run(self, code: str) -> dict:
        started = time.time()
        reason = check_containment(code)
        if reason:
            return {"ok": False, "output": "", "containment_blocked": reason,
                    "elapsed_ms": int((time.time() - started) * 1000)}
        # Safe evaluation of the three demo patterns only, using a regex
        # list literal (never arbitrary code); anything else is "done".
        import ast
        output = ""
        try:
            m = re.search(r"\[([0-9,\s\.\-]+)\]", code)
            vals = ast.literal_eval(m.group(0)) if m else []
            if code.startswith("print(sum(") and "/" not in code:
                output = str(sum(vals))
            elif "sorted(" in code:
                output = str(sorted(vals))
            elif "/" in code and "sum(" in code:
                output = str(sum(vals) / len(vals))
            else:
                output = "done"
        except Exception as exc:  # never leak a host traceback as a result
            return {"ok": False, "output": "", "containment_blocked": f"unsafe pattern: {exc}",
                    "elapsed_ms": int((time.time() - started) * 1000)}
        return {"ok": True, "output": output, "containment_blocked": None,
                "elapsed_ms": int((time.time() - started) * 1000)}

class Verifier:
    def verify(self, task: str, result: dict) -> str:
        if not result["ok"]:
            return f"Blocked by containment: {result['containment_blocked']}. No host action was taken."
        if result["output"] == "":
            return "No verifiable output was produced."
        return f"Verified output: {result['output']}"

def run_task(task: str) -> dict:
    planner, coder, sandbox, verifier = Planner(), Coder(), SandboxExecutor(), Verifier()
    plan = planner.plan(task)
    code = coder.write(task)
    result = sandbox.run(code)
    verdict = verifier.verify(task, result)
    return {"task": task, "plan": plan, "code": code, "result": result, "verdict": verdict}
