"""The stub detector, against both shapes Hugo actually emits.

This file exists because of a specific failure: the detector was written against
unminified output, verified locally against unminified output, and failed in CI
on all 3,260 redirects — because the publish builds with `--minify`, which drops
the attribute quotes it can. A check verified against a different build than the
one that ships is not a check.
"""

import unittest

from check_stubs import STUB

TARGET = "https://anchorframe.app/library/camera/agfa/#ambiflex"

# Copied from real output rather than written by hand, so they stay true to what
# Hugo produces rather than to what this test wishes it produced.
UNMINIFIED = (
    '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n'
    f'\t\t<title>{TARGET}</title>\n'
    '\t\t<link rel="canonical" href="https://anchorframe.app/library/camera/agfa/">\n'
    '\t\t<meta charset="utf-8">\n'
    f'\t\t<meta http-equiv="refresh" content="0; url={TARGET}">\n'
    '\t</head>\n</html>'
)
MINIFIED = (
    '<!doctype html><html lang=en><head>'
    f'<title>{TARGET}</title>'
    '<link rel=canonical href=https://anchorframe.app/library/camera/agfa/>'
    '<meta charset=utf-8>'
    f'<meta http-equiv=refresh content="0; url={TARGET}">'
    '</head></html>'
)
A_REAL_PAGE = (
    '<!doctype html><html lang=en><head><title>Canon AE-1</title></head>'
    '<body><h1>Canon AE-1</h1></body></html>'
)


class StubDetection(unittest.TestCase):
    def test_it_reads_an_unminified_stub(self):
        m = STUB.search(UNMINIFIED)
        self.assertIsNotNone(m, "the plain `hugo` shape is not recognised")
        self.assertEqual(m.group(1), TARGET)

    def test_it_reads_the_minified_stub_the_publish_actually_ships(self):
        m = STUB.search(MINIFIED)
        self.assertIsNotNone(m, "the `hugo --minify` shape is not recognised — "
                                "this is the one that ships")
        self.assertEqual(m.group(1), TARGET)

    def test_both_shapes_yield_the_same_target(self):
        self.assertEqual(STUB.search(UNMINIFIED).group(1), STUB.search(MINIFIED).group(1))

    def test_a_real_page_is_not_mistaken_for_a_stub(self):
        # Without this, a detector that matched everything would pass the two
        # tests above and call the whole site a redirect.
        self.assertIsNone(STUB.search(A_REAL_PAGE))


if __name__ == "__main__":
    unittest.main()
