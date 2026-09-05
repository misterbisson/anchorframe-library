"""The sheet says where each record lives, and refuses to exist if the data does not validate."""

import os
import unittest

from build import sheets
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


if __name__ == "__main__":
    unittest.main()
