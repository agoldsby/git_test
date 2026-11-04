#!/usr/bin/env python3
"""Build ai-tutorial-basics/COURSE.md from the source parts, then zip the course folder.

Usage (from the repository root):
    python3 authoring/build.py

What it does:
1. Joins authoring/src/*.md in filename order.
2. Fills {{COMPANY_CONTEXT}} with the four files in practice-files/company-context/,
   so the tutor's copy of Relay's background always matches the learner's copy.
3. Fills {{ANSWER_KEYS}} with authoring/src/05-answer-keys.md.
4. Writes ai-tutorial-basics/COURSE.md and dist/ai-tutorial-basics.zip.
"""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "authoring" / "src"
COURSE_DIR = ROOT / "ai-tutorial-basics"
CONTEXT_DIR = COURSE_DIR / "practice-files" / "company-context"
DIST = ROOT / "dist"

CONTEXT_ORDER = ["COMPANY.txt", "PRODUCT.txt", "PERSONAS.txt", "COMPETITIVE.txt"]
ANSWER_KEYS = "05-answer-keys.md"


def company_context() -> str:
    parts = ["### Company context files (the learner has these too)\n"]
    for name in CONTEXT_ORDER:
        text = (CONTEXT_DIR / name).read_text(encoding="utf-8").strip()
        # Demote the files' own headings so they nest under this section.
        text = "\n".join("###" + line if line.startswith("#") else line for line in text.splitlines())
        parts.append(f"#### File: company-context/{name}\n\n{text}\n")
    return "\n".join(parts)


def build_course() -> str:
    pieces = []
    for path in sorted(SRC.glob("*.md")):
        if path.name == ANSWER_KEYS:
            continue
        pieces.append(path.read_text(encoding="utf-8").strip() + "\n")
    course = "\n".join(pieces)
    course = course.replace("{{COMPANY_CONTEXT}}", company_context().strip())
    course = course.replace("{{ANSWER_KEYS}}", (SRC / ANSWER_KEYS).read_text(encoding="utf-8").strip())
    leftover = [tok for tok in ("{{COMPANY_CONTEXT}}", "{{ANSWER_KEYS}}") if tok in course]
    if leftover:
        raise SystemExit(f"Unfilled placeholders: {leftover}")
    return course


def make_zip() -> Path:
    DIST.mkdir(exist_ok=True)
    out = DIST / "ai-tutorial-basics.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(COURSE_DIR.rglob("*")):
            if path.is_file() and not path.name.startswith("."):
                zf.write(path, path.relative_to(ROOT))
    return out


if __name__ == "__main__":
    course = build_course()
    (COURSE_DIR / "COURSE.md").write_text(course, encoding="utf-8")
    words = len(course.split())
    print(f"Wrote {COURSE_DIR / 'COURSE.md'} ({words:,} words, ~{int(words * 1.4):,} tokens)")
    print(f"Wrote {make_zip()}")
