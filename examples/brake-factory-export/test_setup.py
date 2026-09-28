"""Integration checks: real converter/installer, isolated project destinations."""

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("factory_setup", HERE / "setup.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="factory-preset-test-")
        cls.root = Path(cls.temp.name)
        cls.built = cls.root / "built"
        cls.manifest = setup.read_manifest()
        setup.build(cls.root / "staging", cls.built, cls.manifest)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_real_conversion_has_only_four_scoped_agents(self):
        files = list((self.built / ".codex/agents").glob("*.toml"))
        self.assertEqual(4, len(files))
        for path in files:
            agent = tomllib.loads(path.read_text())
            self.assertEqual({"name", "description", "developer_instructions"}, set(agent))
            self.assertIn("Factory operating rules", agent["developer_instructions"])
            self.assertNotIn("8-12 touches", agent["developer_instructions"])
        pipeline = json.loads((self.built / "work/pipeline.json").read_text())
        self.assertEqual([], pipeline["buyers"])
        self.assertNotIn("record_templates", pipeline)

    def test_cli_dry_run_does_not_create_target(self):
        target = self.root / "dry run project"
        result = subprocess.run([sys.executable, str(HERE / "setup.py"),
                                 "--project", str(target), "--dry-run"], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(target.exists())

    def test_install_with_spaces_and_rerun_preserve_state(self):
        target = self.root / "installed project"
        command = [sys.executable, str(HERE / "setup.py"), "--project", str(target)]
        result = subprocess.run(command, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        state = target / "work/pipeline.json"
        state.write_text('{"buyers": [{"buyer_id": "B0001"}]}\n')
        unrelated = target / ".codex/agents/existing.toml"
        unrelated.write_text('name = "existing"\n')
        config = target / ".codex/config.toml"
        config.write_text('# existing configuration\n')
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in target.rglob("*") if p.is_file()}
        result = subprocess.run(command, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        for path, digest in before.items():
            self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_conflict_is_detected_before_any_target_write(self):
        target = self.root / "conflict"
        target.mkdir()
        (target / "AGENTS.md").write_text("Keep my instructions.\n")
        result = subprocess.run([sys.executable, str(HERE / "setup.py"),
                                 "--project", str(target)], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(["AGENTS.md"], [p.name for p in target.iterdir()])

    def test_managed_directory_symlink_is_rejected(self):
        target = self.root / "symlink project"
        target.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        (target / ".codex").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            setup.plan_install(self.built, target)
        self.assertEqual([], list(outside.iterdir()))

    def test_manifest_contains_real_source_and_script_pins(self):
        expected = {role["source"] for role in self.manifest["agents"]}
        expected.update({"scripts/convert.sh", "scripts/install.sh", "scripts/lib.sh", "divisions.json", "LICENSE"})
        self.assertEqual(expected, set(self.manifest["source_sha256"]))
        for path, digest in self.manifest["source_sha256"].items():
            self.assertEqual(digest, setup.digest(setup.REPO / path))


if __name__ == "__main__":
    unittest.main()
