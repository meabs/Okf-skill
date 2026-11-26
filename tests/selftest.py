#!/usr/bin/env python3
"""Regression test for the helper scripts. Standard library only (validate.py is run too when PyYAML is installed).
Usage: python3 -I tests/selftest.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / "skills/okf-interview/scripts"
EX = ROOT / "examples/invoice-import/knowledge"
fails = []


def run(*args):
    return subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True)


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


def fresh(tmp, name):
    d = tmp / name
    shutil.copytree(EX, d)
    return d


def sub(path, old, new):
    t = path.read_text()
    assert old in t, (path, old)
    path.write_text(t.replace(old, new, 1))


with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    log = tmp / "log.md"
    log.write_text("## K01 one\n## K02 two\n")
    check("example passes check_links", run(SC / "check_links.py", EX).returncode == 0)
    check("example passes check_content", run(SC / "check_content.py", EX, "--log", log).returncode == 0)
    try:
        import yaml  # noqa: F401
        check("example passes validate --strict", run(SC / "validate.py", EX, "--strict").returncode == 0)
    except ImportError:
        print("skip validate.py (PyYAML not installed)")

    d = fresh(tmp, "broken-link")
    sub(d / "contracts/index.md", "(submission-meaning.md)", "(nope.md)")
    r = run(SC / "check_links.py", d)
    check("check_links flags a dangling link and the orphan", r.returncode == 1 and "broken link" in r.stdout and "not linked" in r.stdout)

    d = fresh(tmp, "placeholder")
    f = d / "contracts/submission-meaning.md"
    f.write_text(f.read_text() + "\nTODO write this\n")
    check("check_content flags TODO", run(SC / "check_content.py", d).returncode == 1)

    d = fresh(tmp, "footnote")
    f = d / "contracts/submission-meaning.md"
    f.write_text(f.read_text() + "\nA claim.[^ghost]\n")
    r = run(SC / "check_content.py", d)
    check("check_content flags undefined footnote", r.returncode == 1 and "ghost" in r.stdout)

    d = fresh(tmp, "dialogue")
    f = d / "contracts/submission-meaning.md"
    f.write_text(f.read_text() + "\nQ1: why? A: because\n")
    check("check_content flags raw dialogue", run(SC / "check_content.py", d).returncode == 1)

    d = fresh(tmp, "limit")
    f = d / "contracts/submission-meaning.md"
    f.write_text(f.read_text() + "\nLimit: recall unknown; see review item K09.\n")
    check("check_content flags unknown review item", run(SC / "check_content.py", d, "--log", log).returncode == 1)
    f.write_text(f.read_text().replace("K09", "K02"))
    check("check_content accepts a known review item", run(SC / "check_content.py", d, "--log", log).returncode == 0)

    d = fresh(tmp, "gap")
    f = d / "contracts/submission-meaning.md"
    f.write_text(f.read_text() + "\nThe procedure was not supplied.\n")
    check("check_content warns on bare gap phrase", "interview-gap" in run(SC / "check_content.py", d).stdout)
    f.write_text(f.read_text().replace("The procedure was not supplied.", 'A rule, for example "was not supplied" or `not established`.\n\nLimit: recall is not established; see review item K02.'))
    r = run(SC / "check_content.py", d, "--log", log)
    check("check_content ignores quoted phrases and Limit paragraphs", "interview-gap" not in r.stdout and r.returncode == 0)

    import hashlib
    pin = (ROOT / "skills/okf-interview/references/UPSTREAM-PIN.txt").read_text()
    check("validate.py still matches the recorded upstream hash", hashlib.sha256((SC / "validate.py").read_bytes()).hexdigest() in pin)

    d = tmp / "scaffold"
    r = run(SC / "new_concept.py", d / "decisions/x.md", "--type", "Decision", "--title", 'A "quoted" title', "--description", "d",
            "--interview", "Interview about x on 2026-01-01; no recording retained", "--code", "Repo at commit abc1234, file y",
            "--by", "process:test", "--index-note", "note")
    text = (d / "decisions/x.md").read_text() if (d / "decisions/x.md").exists() else ""
    check("scaffold writes frontmatter and index entry", r.returncode == 0 and "status: draft" in text and "[A \"quoted\" title](x.md): note" in (d / "decisions/index.md").read_text())
    check("unfilled scaffold is caught by check_content", run(SC / "check_content.py", d).returncode == 1)
    check("scaffold refuses to overwrite", run(SC / "new_concept.py", d / "decisions/x.md", "--type", "T", "--title", "t", "--description", "d",
                                              "--interview", "i", "--code", "c", "--by", "p").returncode != 0)

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
