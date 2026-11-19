#!/usr/bin/env python3
"""Numbers shown on the showcase pages, computed from the repository itself.

    python3 tools/facts.py        # print all facts

Counts come from the file tree, the git history and anchored patterns on the README texts
(the build fails if a sentence they read has changed). Nothing is typed in by hand here.
Standard library only; git is optional (the commit count is reported as None without it).
"""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AS_OF = "2026-11-19"  # date of this showcase restructuring
OLD = "archive/README_2026-11-19_pre-showcase.md"


def p(*a):
    return os.path.join(ROOT, *a)


def read(rel):
    with open(p(rel), encoding="utf-8") as fh:
        return fh.read()


def must(pattern, text, what, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit("facts.py: cannot find %s (pattern %r): the source sentence changed" % (what, pattern))
    return m


def facts():
    f = {"as_of": AS_OF}
    old = read(OLD)

    # structure of the archived README (byte-identical to the repository's README before the restructure)
    f["old_lines"] = str(len(old.split("\n")))
    f["old_h2"] = str(len(re.findall(r"^## ", old, re.M)))

    # sensors: the bullet list under "Supported sensors"
    sens = must(r"\*\*Supported sensors[^\n]*\n\n((?:- [^\n]+\n)+)", old, "sensor list").group(1)
    f["sensor_types"] = str(len(re.findall(r"^- ", sens, re.M)))
    f["channels_min"] = must(r"Minimum / Минимум: (\d+) channels", old, "minimum channels").group(1)
    f["channels_target"] = must(r"Target / Цель: (\d+)–(\d+) channels", old, "target channels").group(2)
    f["channels_target_min"] = must(r"Target / Цель: (\d+)–(\d+) channels", old, "target channels").group(1)

    # measurement core and roadmap
    f["resolution_ps"] = must(r"Resolution / Разрешение: ≤ (\d+)–(\d+) ps", old, "resolution").group(2)
    f["resolution_ps_min"] = must(r"Resolution / Разрешение: ≤ (\d+)–(\d+) ps", old, "resolution").group(1)
    f["phases"] = str(len(re.findall(r"^\| \*\*Phase \d", old, re.M)))
    f["phases_started"] = "0" if "None of these phases have started yet" in old else "?"
    f["roadmap_p1_channels"] = must(r"Phase 1 / Фаза 1\*\* \| (\d+)–(\d+) channels", old, "phase 1 channels").group(2)

    # issue template
    f["issue_min_channels"] = must(r"Support ≥ (\d+) channels", old, "issue min channels").group(1)
    f["issue_phase_ps"] = must(r"Phase resolution ≤ (\d+) ps", old, "issue phase resolution").group(1)

    # ecosystem and applications listed in the README (context only)
    eco = must(r"## ASRP ECOSYSTEM.*?(?=\n## CONTACT)", old, "ecosystem section", re.S).group(0)
    f["eco_repos"] = str(len(re.findall(r"^\| \*\*[^|]+\*\* \| [^|]+ \| \[View[^\]]*\]\(https://github\.com/AdvancedScientificResearchProjects/", eco, re.M)))
    f["patent_rows"] = str(len(re.findall(r"^\| \*\*[^|]+\*\* \| KZ ", eco, re.M)))
    f["patron_tiers"] = must(r"(\d) patron tiers", old, "patron tiers").group(1)
    f["data_levels"] = str(len(re.findall(r"^\| \*\*(PUBLIC|RESEARCH|RESTRICTED|INTERNAL)", old, re.M)))

    # this repository
    files = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
        files += [os.path.relpath(os.path.join(dp, x), ROOT) for x in fn]
    f["repo_files"] = str(len([x for x in files if not x.startswith(("guide", "tools", "tests", "archive"))]))
    f["content_pages"] = str(len([x for x in files if x.startswith("guide/") and x.endswith(".md")]))
    try:
        n = subprocess.run(["git", "rev-list", "--count", "main"], cwd=ROOT, capture_output=True, text=True, check=True)
        f["commits_main"] = n.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        f["commits_main"] = None
    return f


if __name__ == "__main__":
    for k, v in facts().items():
        print("%-22s %s" % (k, v))
