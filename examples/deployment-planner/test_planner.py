import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from planner import plan, PolicyError, unique_pairs, reject_constant

HERE = Path(__file__).resolve().parent
POLICY = json.loads((HERE / "deployments.yaml").read_text())
ROOT = HERE / "fixtures"

class PlannerTests(unittest.TestCase):
    def test_order_and_reporting(self):
        paths = ["stacks/application/compose.yaml", "stacks/platform/compose.yaml",
                 "stacks/manual/compose.yaml", "README.md"]
        self.assertEqual(plan(POLICY, paths, ROOT), json.loads((HERE / "sample-output.json").read_text()))
        self.assertEqual(plan(POLICY, paths[::-1], ROOT), plan(POLICY, paths, ROOT))

    def test_unchanged_dependency(self):
        self.assertEqual(plan(POLICY, ["stacks/application/compose.yaml"], ROOT)["deploy"], ["application"])

    def test_docs_only(self):
        result = plan(POLICY, ["stacks/platform/README.md", "README.md"], ROOT)
        self.assertEqual(result["deploy"], [])
        self.assertEqual(len(result["ignored"]), 2)

    def test_excluded(self):
        self.assertEqual(plan(POLICY, ["stacks/manual/compose.yaml"], ROOT)["excluded"], ["manual"])

    def test_unknown(self):
        with self.assertRaises(PolicyError):
            plan(POLICY, ["stacks/unknown/compose.yaml"], ROOT)

    def test_missing_compose(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(PolicyError):
                plan(POLICY, ["stacks/platform/compose.yaml"], tmp)

    def test_invalid_paths(self):
        for path in ("../secret", "/absolute", "stacks//platform/compose.yaml", "C:/path", "stacks/../x"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                plan(POLICY, [path], ROOT)

    def test_cycle(self):
        policy = copy.deepcopy(POLICY)
        policy["stacks"]["platform"]["after"] = ["application"]
        with self.assertRaises(PolicyError):
            plan(policy, [], ROOT)

    def test_unknown_dependency(self):
        policy = copy.deepcopy(POLICY)
        policy["stacks"]["platform"]["after"] = ["unknown"]
        with self.assertRaises(PolicyError):
            plan(policy, [], ROOT)

    def test_double_classification(self):
        policy = copy.deepcopy(POLICY)
        policy["excluded"]["platform"] = "Conflict"
        with self.assertRaises(PolicyError):
            plan(policy, [], ROOT)

    def test_duplicate_key(self):
        with self.assertRaises(PolicyError):
            json.loads('{"a": 1, "a": 2}', object_pairs_hook=unique_pairs)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            target = root / "stacks/platform"
            target.mkdir(parents=True)
            outside = Path(tmp) / "outside.yaml"
            outside.write_text("services: {}")
            (target / "compose.yaml").symlink_to(outside)
            with self.assertRaises(PolicyError):
                plan(POLICY, ["stacks/platform/compose.yaml"], root)

    def test_duplicate_changes(self):
        path = "stacks/platform/compose.yaml"
        self.assertEqual(plan(POLICY, [path, path], ROOT), plan(POLICY, [path], ROOT))

    def test_duplicate_dependencies(self):
        policy = copy.deepcopy(POLICY)
        policy["stacks"]["application"]["after"] = ["platform", "platform"]
        with self.assertRaises(PolicyError):
            plan(policy, [], ROOT)

    def test_invalid_policy_shapes(self):
        for policy in (None, [], {}, {"stacks": [], "excluded": {}},
                       {"stacks": {"x": {"after": [1]}}, "excluded": {}},
                       {"stacks": {}, "excluded": {"x": ""}}):
            with self.subTest(policy=policy), self.assertRaises(PolicyError):
                plan(policy, [], ROOT)

    def test_control_characters(self):
        for path in ("stacks/platform/a\x00", "docs/a\n.md", "docs/a\x7f"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                plan(POLICY, [path], ROOT)

    def test_invalid_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            for root in (Path(tmp) / "missing", HERE / "planner.py"):
                with self.assertRaises(PolicyError):
                    plan(POLICY, [], root)

    def test_symlink_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "stacks/platform"
            target.mkdir(parents=True)
            (target / "compose.yaml").symlink_to("compose.yaml")
            with self.assertRaises(PolicyError):
                plan(POLICY, ["stacks/platform/compose.yaml"], tmp)

    def test_nonstandard_json(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(PolicyError):
                json.loads(value, parse_constant=reject_constant)

    def test_cli_error(self):
        result = subprocess.run([sys.executable, str(HERE / "planner.py"), "--manifest",
            str(HERE / "deployments.yaml"), "--root", str(ROOT), "stacks/unknown/compose.yaml"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stderr))

if __name__ == "__main__":
    unittest.main()
