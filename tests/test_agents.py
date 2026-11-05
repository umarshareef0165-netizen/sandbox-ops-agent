import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from agents import run_task, SandboxExecutor, check_containment

class TestAgents(unittest.TestCase):
    def test_sum_task(self):
        r = run_task("Add up 12, 28 and 40")
        self.assertTrue(r["result"]["ok"]); self.assertEqual(r["result"]["output"], "80")
    def test_sort_task(self):
        r = run_task("Sort 5, 2, 9, 1")
        self.assertEqual(r["result"]["output"], "[1, 2, 5, 9]")
    def test_average_task(self):
        r = run_task("Find the average of 10, 20, 30")
        self.assertEqual(r["result"]["output"], "20.0")
    def test_empty_task_rejected(self):
        with self.assertRaises(ValueError):
            run_task("   ")
    def test_containment_rm(self):
        self.assertEqual(check_containment("rm -rf /"), "destructive delete")
    def test_containment_network(self):
        self.assertEqual(check_containment("curl https://example.com"), "network access")
    def test_containment_traversal(self):
        self.assertEqual(check_containment("open('../../etc/passwd')"), "path traversal")
    def test_blocked_execution_never_runs(self):
        r = SandboxExecutor().run("rm -rf /")
        self.assertFalse(r["ok"]); self.assertIsNotNone(r["containment_blocked"])
    def test_plan_has_five_steps(self):
        self.assertEqual(len(run_task("Sort 5, 2, 9, 1")["plan"]), 5)

if __name__ == "__main__":
    unittest.main()
