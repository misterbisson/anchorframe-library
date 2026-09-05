"""The sheets and the redirect manifest, checked against the real corpus."""

import os
import unittest

from build import redirects, sheets
from content import load
from validate import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Build(unittest.TestCase):
    def test_the_real_corpus_validates(self):
        self.assertEqual(validate(ROOT), [])

    def test_every_entry_carries_the_url_it_will_be_served_at(self):
        for kind, sheet in sheets(ROOT).items():
            self.assertTrue(sheet["entries"], f"{kind} is empty")
            for e in sheet["entries"]:
                self.assertTrue(e["url"].startswith(f"/library/{kind}/"), e["url"])
                # No dots: the site's router reads one as a file extension and
                # never appends /index.html. See tools/slug.py.
                self.assertNotIn(".", e["url"])

    def test_every_sheet_carries_its_licence(self):
        for kind, sheet in sheets(ROOT).items():
            self.assertEqual(sheet["license"], "CC-BY-SA-4.0")
            self.assertIn("Wikipedia", sheet["attribution"])


class Redirects(unittest.TestCase):
    def setUp(self):
        self.r = redirects(ROOT)
        self.records = {x.url: x for x in load(ROOT)[0]}

    def test_a_provisional_redirect_points_at_its_own_row_in_its_brand_list(self):
        for row in self.r["provisional"]:
            rec = self.records[row["from"]]
            self.assertEqual(row["to"],
                             f"/library/{rec.kind}/{rec.brand_slug}#{rec.slug}")

    def test_only_records_with_nothing_to_show_redirect(self):
        # The whole point of computing this rather than maintaining it: a record
        # leaves the list by gaining content, not by anyone editing the list.
        provisional = {row["from"] for row in self.r["provisional"]}
        for url, rec in self.records.items():
            self.assertEqual(rec.promoted, url not in provisional, url)

    def test_a_permanent_redirect_never_shadows_a_record(self):
        for row in self.r["permanent"]:
            self.assertNotIn(row["from"], self.records)
            self.assertIn(row["to"], self.records)

    def test_no_address_redirects_twice(self):
        froms = [row["from"] for row in self.r["permanent"] + self.r["provisional"]]
        self.assertEqual(len(froms), len(set(froms)))


if __name__ == "__main__":
    unittest.main()
