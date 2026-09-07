"""The README's counts are checked, not trusted.

Between #8 and #28 four of them drifted while nobody looked: lenses by 23, film
brands by 5, film photographs from five to seventy, and a bullet saying the
corpus held no film detail survived the two releases that added it. A number in
a README is the first thing a reader trusts, which makes a stale one worse than
no number at all.
"""

import os
import unittest

import readme_counts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Counts(unittest.TestCase):
    def test_the_readme_block_matches_the_corpus(self):
        text = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
        self.assertIn(readme_counts.START, text)
        block = readme_counts.START + \
            text.split(readme_counts.START, 1)[1].split(readme_counts.END, 1)[0] + \
            readme_counts.END
        self.assertEqual(readme_counts.render(readme_counts.counts(ROOT)), block,
                         "README counts are stale; run "
                         "`python3 tools/readme_counts.py --write`")

    def test_the_generated_block_reports_every_kind(self):
        # A kind added to the corpus and not to the table would leave the README
        # quietly describing a smaller repository than the one it ships with.
        c = readme_counts.counts(ROOT)
        from content import KINDS
        self.assertEqual(len(KINDS), len(c["kinds"]))

    def test_a_changed_corpus_makes_the_check_fail(self):
        # The mutation: if render() ignored its input, the test above would pass
        # against anything.
        c = readme_counts.counts(ROOT)
        c["kinds"][0]["records"] += 1
        self.assertNotEqual(readme_counts.render(readme_counts.counts(ROOT)),
                            readme_counts.render(c))


if __name__ == "__main__":
    unittest.main()
