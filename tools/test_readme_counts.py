"""The README's counts are generated, so what is tested is the generator.

Between #8 and #28 four of them drifted while nobody looked: lenses by 23, film
brands by 5, film photographs from five to seventy, and a bullet saying the
corpus held no film detail survived the two releases that added it. A number in
a README is the first thing a reader trusts, which makes a stale one worse than
no number at all. That is still true, and it is still enforced — by
`.github/workflows/counts.yml`, which regenerates the block on main after the
merge that moved it.

**What used to be here was an assertion that the committed block is current, and
it sent the bill to the wrong person.** Every pull request that adds a record
changes a count, so every content pull request failed until someone ran
`readme_counts.py --write` — a generator CONTRIBUTING.md does not mention, for
numbers the contributor did not type, in a file that opens by promising that
adding a record "needs you to run nothing". On a fork, where `check` is the only
thing that reports back, that red tick was the first thing a first-time
contributor saw.

A count of this corpus has no judgement in it; `check_stubs.py` reconciles a
claim a person made, and that is the distinction the old comment here missed
when it borrowed its reasoning. A derived number belongs in a generator's
output, not in a contributor's checklist.

So the staleness assertion is gone and these tests cover what is left to get
wrong: that the generator reads the corpus, that it reports every kind, and
that the markers it writes between are still in the file.
"""

import os
import unittest

import readme_counts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Counts(unittest.TestCase):
    def test_the_block_the_generator_writes_into_is_still_there(self):
        # Not a staleness check — the numbers are regenerated on main. This is
        # the one thing a hand edit can still break: `--write` needs both
        # markers to find its block, and without them it has nowhere to put the
        # table and the README would quietly stop carrying counts at all.
        text = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
        self.assertIn(readme_counts.START, text)
        self.assertIn(readme_counts.END, text)
        self.assertLess(text.index(readme_counts.START), text.index(readme_counts.END))

    def test_the_generator_reads_the_corpus_it_is_pointed_at(self):
        # `counts()` must not be reporting constants. The staleness assertion
        # used to prove this incidentally; now it is proven on purpose.
        c = readme_counts.counts(ROOT)
        self.assertGreater(c["kinds"][0]["records"], 0)
        self.assertIn(readme_counts.START, readme_counts.render(c))

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
