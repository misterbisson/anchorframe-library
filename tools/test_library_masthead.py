"""Every page here offers a way back to the site this is a section of.

`baseURL` in hugo.toml is `https://anchorframe.app/library/` -- this section's
root, not the site's. Nothing in a template could reach the apex without naming
it separately, and for months nothing did: every page linked back only to
/library/, and the site itself linked here not at all, so the two halves of one
hostname could not reach each other.

Nothing 404s when that is true and no build goes red, which is why it lasted.
The visible cost is a visitor who lands on a camera from a search engine and has
no path to the app this index exists to serve -- and this is the part of
anchorframe.app with the pages a search engine has any reason to return.

**The other half of this pin lives in a repository this one cannot read.**
`misterbisson/anchorframe-site` carries the inbound link (Library in its nav and
footer) and pins APEX below as its expectation of this side, in
`tools/test_library_link.py`. Both repositories assert the identical literal,
neither can see the other, and either one drifting turns its own side red. Same
arrangement, and the same reason, as the OIDC subject in test_deploy_subject.py.

What this cannot do is prove the apex answers. `tools/check_stubs.py` checks
links into *this* site and skips absolute URLs by construction, which is correct
-- a link checker that fetched the wider web would fail on somebody else's
outage. What does check it is deploy.yml, which curls /privacy and /support on
every publish because this job shares a distribution with them.

Dependency-free on purpose: regex over two files, so it runs anywhere python3
does and a fork's pull request gets the same green tick as anyone else's.
"""

from __future__ import annotations

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = ROOT / "hugo.toml"
BASEOF = ROOT / "layouts" / "_default" / "baseof.html"

# What anchorframe-site's tools/test_library_link.py pins as this side's return
# link. Change both or neither.
APEX = "https://anchorframe.app/"

# The param the templates go through, so the literal is written once.
PARAM = "site.Params.app"

MASTHEAD = re.compile(r'<header class="masthead">(.*?)</header>', re.S)
FOOTER = re.compile(r"<footer>(.*?)</footer>", re.S)


class Masthead(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CONFIG.is_file(), "no hugo.toml")
        self.assertTrue(BASEOF.is_file(), "no baseof.html")
        self.config = CONFIG.read_text(encoding="utf-8")
        self.baseof = BASEOF.read_text(encoding="utf-8")

    def test_the_apex_is_configured_exactly(self):
        m = re.search(r'^\s*app\s*=\s*"([^"]+)"', self.config, re.M)
        self.assertIsNotNone(m, "hugo.toml defines no params.app; nothing can link out")
        self.assertEqual(
            m.group(1), APEX,
            "params.app has drifted from the literal anchorframe-site pins in "
            "tools/test_library_link.py. Change it in both repositories or neither.",
        )

    def test_the_baseurl_is_still_the_subpath(self):
        """Guard the premise: if baseURL became the apex, this whole check is moot."""
        m = re.search(r'^baseURL\s*=\s*"([^"]+)"', self.config, re.M)
        self.assertIsNotNone(m, "hugo.toml has no baseURL")
        self.assertEqual(
            m.group(1), "https://anchorframe.app/library/",
            "baseURL moved. This site is published under a prefix of another "
            "site by anchorframe-site's IAM policy, which permits exactly "
            "`library/` -- a build at a different base would upload to a path "
            "the publish role cannot write.",
        )

    def test_the_masthead_links_out(self):
        m = MASTHEAD.search(self.baseof)
        self.assertIsNotNone(m, "no masthead in baseof.html; the parser found nothing to check")
        self.assertIn(
            PARAM, m.group(1),
            "the masthead does not link the apex. It is the only element on "
            "every page of this site, including the home page, where the "
            "breadcrumbs are not rendered.",
        )

    def test_the_footer_says_what_this_is_for(self):
        m = FOOTER.search(self.baseof)
        self.assertIsNotNone(m, "no footer in baseof.html")
        self.assertIn(
            PARAM, m.group(1),
            "the footer no longer names the app. A reader who reached a lens "
            "from a search engine has no other way to learn what this index is.",
        )

    def test_the_stub_template_is_not_expected_to_carry_links(self):
        """A record with nothing to show emits a bare meta-refresh, by design.

        Asserted so the next person reading this file does not add the masthead
        check to that branch and wonder why it fails: that page has no body at
        all, and giving it one would make a redirect look like a destination.
        """
        self.assertIn("http-equiv", self.baseof)
        stub = self.baseof.split("{{- else -}}")[0]
        self.assertNotIn(PARAM, stub, "the stub branch grew a link; it has no body to put one in")


if __name__ == "__main__":
    unittest.main()
