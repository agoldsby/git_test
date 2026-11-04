#!/usr/bin/env python3
"""Package the AI Agent Basics course for sharing.

Usage (from the repository root):
    python3 authoring/build.py

What it does:
1. Copies ai-agent-basics/AGENTS.md to ai-agent-basics/CLAUDE.md, so both AI apps find
   identical instructions. (Edit AGENTS.md only.)
2. Checks that every course file path mentioned in the instructions actually exists.
3. Zips the ai-agent-basics/ folder (with the folder at the top level) into
   dist/ai-agent-basics.zip. That zip is what learners upload.
"""
from pathlib import Path
import re
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "ai-agent-basics"
DIST = ROOT / "dist"

# Files the AI creates during the course; they must NOT ship in the zip.
CREATED_DURING_COURSE = {
    "feedback-synthesis.md",
    "research-communications.md",
    "dashboard-talking-points.md",
    "onboarding-research.md",
    "my-relay-work.zip",
}


def sync_claude_md() -> None:
    shutil.copyfile(COURSE / "AGENTS.md", COURSE / "CLAUDE.md")


def check_references() -> list[str]:
    """Find backticked paths like `company-context/COMPANY.md` and make sure they exist."""
    problems = []
    for script in [COURSE / "AGENTS.md", *COURSE.glob("lesson-modules/*/MODULE.md")]:
        text = script.read_text(encoding="utf-8")
        for ref in set(re.findall(r"`([\w./-]+\.(?:md|png))`", text)):
            name = Path(ref).name
            if name in CREATED_DURING_COURSE or name in {"CLAUDE.md"}:
                continue
            # Accept a full path from the course root, or any file whose path ends with it.
            found = (COURSE / ref).exists() or any(
                f.as_posix().endswith("/" + ref) for f in COURSE.rglob("*") if f.is_file()
            )
            if not found:
                problems.append(f"{script.relative_to(ROOT)} mentions missing file `{ref}`")
    return problems


def check_no_leftovers() -> list[str]:
    return [
        f"{p.relative_to(ROOT)} is created during the course and shouldn't be shipped"
        for p in COURSE.rglob("*")
        if p.name in CREATED_DURING_COURSE
    ]


def make_zip() -> Path:
    DIST.mkdir(exist_ok=True)
    out = DIST / "ai-agent-basics.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(COURSE.rglob("*")):
            if path.is_file() and not path.name.startswith("."):
                zf.write(path, path.relative_to(ROOT))
    return out


if __name__ == "__main__":
    sync_claude_md()
    problems = check_references() + check_no_leftovers()
    if problems:
        print("Build stopped:\n  " + "\n  ".join(problems))
        sys.exit(1)
    out = make_zip()
    count = len(zipfile.ZipFile(out).namelist())
    print(f"Wrote {out.relative_to(ROOT)} ({count} files, {out.stat().st_size // 1024} KB)")
