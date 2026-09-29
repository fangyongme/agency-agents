#!/usr/bin/env python3
"""Build a four-agent project through the repository's existing converters."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ is required (stdlib tomllib); no pip packages needed.")
import tomllib

PRESET = Path(__file__).resolve().parent
REPO = PRESET.parent.parent
PRIVATE_SEEDS = {Path("knowledge/factory-profile.json"), Path("work/pipeline.json")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args):
    result = subprocess.run(args, text=True, capture_output=True, cwd=REPO)
    if result.returncode:
        raise RuntimeError(f"Command failed: {args[0]}\n{result.stdout}\n{result.stderr}")


def read_manifest():
    manifest = json.loads((PRESET / "manifest.json").read_text(encoding="utf-8"))
    selection = [line.split("#", 1)[0].strip() for line in
                 (PRESET / "agents.txt").read_text().splitlines()]
    selection = [line for line in selection if line]
    slugs = [role["slug"] for role in manifest["agents"]]
    if len(slugs) != 4 or selection != slugs or len(set(slugs)) != 4:
        raise ValueError("Manifest and agents.txt must select exactly the same four agents.")
    for role in manifest["agents"]:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", role["slug"]):
            raise ValueError("Invalid agent slug")
        for key in ("source", "role"):
            root = REPO if key == "source" else PRESET
            path = (root / role[key]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError(f"Invalid {key} path: {role[key]}")
    for relative, expected in manifest["source_sha256"].items():
        path = (REPO / relative).resolve()
        if not path.is_relative_to(REPO) or not path.is_file() or digest(path) != expected:
            raise ValueError(
                f"Upstream source changed: {relative}. Review the diff and role adaptation, "
                "then deliberately update manifest.json; no silent regeneration.")
    return manifest


def build(stage, output, manifest):
    # An isolated source tree allows the unmodified converter to see only four
    # tailored bodies. The upstream roster and generated integrations stay intact.
    for relative in ("scripts/convert.sh", "scripts/install.sh", "scripts/lib.sh", "divisions.json"):
        dest = stage / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / relative, dest)
    common = (PRESET / "project/OPERATING-RULES.md").read_text(encoding="utf-8")
    for role in manifest["agents"]:
        body = (PRESET / role["role"]).read_text(encoding="utf-8")
        source = stage / role["source"]
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "---\nname: " + json.dumps(role["name"]) +
            "\ndescription: " + json.dumps(role["description"]) +
            "\n---\n\n" + common + "\n" + body, encoding="utf-8")
    run("bash", str(stage / "scripts/convert.sh"), "--tool", "codex")
    shutil.copytree(PRESET / "project", output)
    run("bash", str(stage / "scripts/install.sh"), "--tool", "codex",
        "--agents-file", str(PRESET / "agents.txt"), "--no-interactive", "--no-convert",
        "--path", str(output / ".codex/agents"))
    files = sorted((output / ".codex/agents").glob("*.toml"))
    expected = {r["slug"] + ".toml": r for r in manifest["agents"]}
    if {p.name for p in files} != set(expected):
        raise ValueError("Converter did not produce exactly the selected four files.")
    for path in files:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
        role = expected[path.name]
        if set(parsed) != {"name", "description", "developer_instructions"}:
            raise ValueError(f"Unexpected Codex format: {path.name}")
        if parsed["name"] != role["name"] or parsed["description"] != role["description"]:
            raise ValueError(f"Incorrect agent identity: {path.name}")
        if not parsed["developer_instructions"].strip():
            raise ValueError(f"Empty instructions: {path.name}")
    shutil.copy2(REPO / "LICENSE", output / "AGENCY-LICENSE.txt")
    (output / "SOURCE-MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.copy2(output / "knowledge/factory-profile.example.json",
                 output / "knowledge/factory-profile.json")
    pipeline = json.loads((output / "templates/pipeline.json").read_text())
    pipeline.pop("record_templates")
    (output / "work").mkdir()
    (output / "work/pipeline.json").write_text(json.dumps(pipeline, indent=2) + "\n")


def plan_install(output, target):
    writes = []
    for source in sorted(p for p in output.rglob("*") if p.is_file()):
        relative = source.relative_to(output)
        dest = target / relative
        # Refuse symlinked managed paths, including a symlinked .codex directory.
        for part in (dest, *dest.parents):
            if part == target.parent:
                break
            if part.is_symlink():
                raise ValueError(f"Refusing symlinked managed path: {part}")
            if part != dest and part.exists() and not part.is_dir():
                raise ValueError(f"Parent is not a directory: {part}")
        if dest.exists():
            if not dest.is_file():
                raise ValueError(f"Destination is not a file: {dest}")
            if relative in PRIVATE_SEEDS:
                continue  # Operational state is never reset by setup.
            if dest.read_bytes() != source.read_bytes():
                raise ValueError(f"Existing file differs: {dest}. Generate a new sibling project and review the diff.")
        else:
            writes.append((source, dest))
    return writes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True,
                        help="Destination Codex project (prefer a new directory)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate/build in temporary storage; do not write the destination")
    args = parser.parse_args()
    raw_target = args.project.expanduser().absolute()
    if raw_target.is_symlink():
        raise ValueError("Project destination must not be a symlink.")
    target = raw_target.resolve()
    if target.exists() and not target.is_dir():
        raise ValueError("Project destination must be a directory.")
    # Keep this public source checkout separate from operational customer data.
    if target == REPO or target.is_relative_to(PRESET):
        raise ValueError("Use a separate project directory, not the source repository or preset.")
    manifest = read_manifest()
    with tempfile.TemporaryDirectory(prefix="brake-factory-") as temporary:
        temporary = Path(temporary)
        output = temporary / "project"
        build(temporary / "staging-repo", output, manifest)
        writes = plan_install(output, target)  # Check every conflict before target writes.
        if args.dry_run:
            print(f"Validated four Codex agents; would create {len(writes)} files in {target}")
            return
        created = []
        try:
            for source, dest in writes:
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as handle:  # Never overwrite even after a concurrent change.
                    created.append(dest)
                    handle.write(source.read_bytes())
        except Exception:
            for dest in reversed(created):
                dest.unlink()
            raise
    print(f"Ready: {target} ({len(writes)} new files; exactly four preset agents).")
    print("Open this directory in Codex, start a new session, and read START-HERE.md.")
    print("Existing unrelated agents/configs are preserved; this installs no global agents.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
