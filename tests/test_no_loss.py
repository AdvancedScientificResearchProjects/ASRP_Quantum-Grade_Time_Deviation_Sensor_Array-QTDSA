"""Regression gate for the showcase pages.

The restructured pages must keep every element of the archived README (hard checks in tools/verify_no_loss.py),
no existing content file may change, every diagram must have a language twin and metadata, the badge numbers must
equal tools/facts.py, and English pages must not carry Cyrillic prose.

Run from the repository root:  python3 -m unittest discover -s tests -v
"""
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import facts as factsmod  # noqa: E402


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def run(*args):
    return subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True, text=True)


def guide_pages():
    g = os.path.join(ROOT, "guide")
    return sorted(n for n in os.listdir(g) if n.endswith(".md"))


class NoLossTest(unittest.TestCase):
    def test_hard_checks_pass(self):
        r = run("tools/verify_no_loss.py")
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertIn("RESULT: PASS", r.stdout)

    def test_archive_is_byte_identical_to_the_tag(self):
        tagged = subprocess.run(["git", "show", "pre-showcase-2026-11:README.md"], cwd=ROOT, capture_output=True)
        if tagged.returncode != 0:
            self.skipTest("tag pre-showcase-2026-11 not available")
        with open(os.path.join(ROOT, "archive/README_2026-11-19_pre-showcase.md"), "rb") as fh:
            self.assertEqual(fh.read(), tagged.stdout)


class VisualsTest(unittest.TestCase):
    def test_visuals_build_and_fit(self):
        """The generator aborts when a label does not fit its box or a font is below 12 px."""
        r = run("tools/build_visuals.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_svg_has_a_language_twin_and_metadata(self):
        for d in ("guide/assets/banner", "guide/assets/diagrams"):
            names = sorted(os.listdir(os.path.join(ROOT, d)))
            self.assertTrue(names, d)
            for n in names:
                twin = n.replace(".en.svg", ".ru.svg") if n.endswith(".en.svg") else n.replace(".ru.svg", ".en.svg")
                self.assertIn(twin, names, "missing language twin for " + n)
                svg = read(os.path.join(d, n))
                for need in ("<title", "<desc", "viewBox", 'role="img"'):
                    self.assertIn(need, svg, n + " lacks " + need)


class FactsTest(unittest.TestCase):
    def test_badges_equal_computed_facts(self):
        F = factsmod.facts()
        en = read("README.md")
        ru = read("README.ru.md")
        self.assertIn("sensor_types-%s-" % F["sensor_types"], en)
        self.assertIn("channels-%s%%E2%%80%%93%s_(design_target)" % (F["channels_min"], F["channels_target"]), en)
        self.assertIn("roadmap-0_of_%s_phases_started" % F["phases"], en)
        self.assertIn("типы_датчиков-%s-" % F["sensor_types"], ru)
        self.assertIn("каналы-%s%%E2%%80%%93%s_(проектная_цель)" % (F["channels_min"], F["channels_target"]), ru)
        self.assertIn("0_из_%s_фаз_начато" % F["phases"], ru)

    def test_stated_values_equal_computed_facts(self):
        F = factsmod.facts()
        text = read("guide/DESIGN.md")
        self.assertIn("Minimum: %s channels" % F["channels_min"], text)
        self.assertIn("Target: %s–%s channels" % (F["channels_target_min"], F["channels_target"]), text)
        self.assertIn("Resolution: ≤ %s–%s ps" % (F["resolution_ps_min"], F["resolution_ps"]), text)
        self.assertIn("Phase resolution ≤ %s ps" % F["issue_phase_ps"], text)
        self.assertEqual(F["phases"], "4")
        self.assertEqual(F["patron_tiers"], "7")

    def test_nothing_is_marked_as_measured(self):
        """No page may describe a value as measured or validated: the repository has no measurement."""
        for f in ["README.md", "README.ru.md"] + ["guide/" + n for n in guide_pages()]:
            text = read(f).lower()
            for bad in ("we measured", "we validated", "achieved resolution", "measured resolution of"):
                self.assertNotIn(bad, text, "%s claims a result: %r" % (f, bad))


class PagesTest(unittest.TestCase):
    def test_every_guide_page_has_a_twin_and_backlinks(self):
        names = guide_pages()
        for name in names:
            twin = name[:-6] + ".md" if name.endswith(".ru.md") else name[:-3] + ".ru.md"
            self.assertIn(twin, names, "missing language twin for " + name)
            head = read("guide/" + name).split("\n")[:4]
            self.assertIn(twin, head[0], "no language switch on line 1 of " + name)
            self.assertIn("README", head[2], "no back-link on line 3 of " + name)

    def test_readme_twins_have_language_switch(self):
        self.assertIn("README.ru.md", read("README.md").split("\n")[2])
        self.assertIn("README.md", read("README.ru.md").split("\n")[0])

    def test_english_pages_carry_no_cyrillic_prose(self):
        """English pages have no Cyrillic prose. Code, links and HTML anchors are skipped."""
        files = ["README.md"] + ["guide/" + n for n in guide_pages() if not n.endswith(".ru.md")]
        for f in files:
            text = read(f)
            text = re.sub(r"```.*?```|`[^`]*`|<[^>]+>|\[[^\]]*\]\([^)]*\)", "", text, flags=re.S)
            for ln in text.split("\n"):
                self.assertIsNone(re.search(r"[А-Яа-яЁё]{3,}", ln), "Cyrillic in English page %s: %s" % (f, ln[:100]))

    def test_only_the_two_readmes_changed_among_existing_files(self):
        """H9 in code: no existing content file other than README.md and README.ru.md differs from the tag."""
        r = subprocess.run(["git", "diff", "--name-only", "--diff-filter=MDRT", "pre-showcase-2026-11"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            self.skipTest("tag pre-showcase-2026-11 not available")
        changed = [x for x in r.stdout.split() if x]
        self.assertTrue(set(changed) <= {"README.md", "README.ru.md"}, changed)


if __name__ == "__main__":
    unittest.main()
