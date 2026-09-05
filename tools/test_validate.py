"""Each guard, mutated until it fails.

A guard no test can break is a guard nobody can prove. Every test here starts
from a fixture that validates cleanly, makes one change, and asserts that the
named rule — not merely *some* rule — objects.
"""

import json
import os
import shutil
import tempfile
import unittest

from validate import validate


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        d = os.path.join(self.root, "data")
        write(f"{d}/mount/canon-fd.json",
              {"name": "Canon FD", "brand": "Canon", "spellings": ["Canon FD"]})
        write(f"{d}/mount/m42.json", {"name": "M42", "spellings": ["M42 screw mount"]})
        write(f"{d}/camera/canon/ae-1.json",
              {"name": "Canon AE-1", "brand": "Canon", "mount": "canon-fd",
               "source": "https://en.wikipedia.org/wiki/Canon_AE-1"})
        write(f"{d}/camera/canon/trip-35.json",
              {"name": "Canon Trip 35", "brand": "Canon", "lens": "Zuiko 40mm",
               "source": "https://en.wikipedia.org/wiki/Canon_Trip"})
        write(f"{d}/film/kodak/portra-400.json",
              {"name": "Kodak Portra 400", "brand": "Kodak", "discontinued": False,
               "source": "https://en.wikipedia.org/wiki/List_of_photographic_films#Kodak"})
        write(f"{d}/lens/nikon/nikkor-45mm-f2-8e-ed.json",
              {"name": "Nikkor 45mm f/2.8E ED", "brand": "Nikon", "mount": "canon-fd",
               "alternates": [{"brand": "nikkor", "slug": "45mm-f2-8e-ed"}],
               "source": "https://en.wikipedia.org/wiki/Nikon_F-mount"})
        self.cam = f"{d}/camera/canon/ae-1.json"
        self.film = f"{d}/film/kodak/portra-400.json"
        self.lens = f"{d}/lens/nikon/nikkor-45mm-f2-8e-ed.json"

    def edit(self, path, **changes):
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
        for k, v in changes.items():
            if v is None:
                rec.pop(k, None)
            else:
                rec[k] = v
        write(path, rec)

    def assertObjects(self, needle):
        problems = validate(self.root)
        self.assertTrue(any(needle in p for p in problems),
                        f"nothing objected to {needle!r}; got {problems}")

    def test_the_fixture_itself_is_clean(self):
        # Without this, every test below could be passing for the wrong reason.
        self.assertEqual(validate(self.root), [])

    def test_a_missing_name_is_caught(self):
        self.edit(self.cam, name=None)
        self.assertObjects("name is required")

    def test_an_unknown_field_is_caught(self):
        self.edit(self.cam, iso=400)
        self.assertObjects("unknown field")

    def test_a_brand_that_disagrees_with_its_directory_is_caught(self):
        self.edit(self.cam, brand="Nikon")
        self.assertObjects("not 'canon'")

    def test_a_slug_that_does_not_follow_from_the_name_is_caught(self):
        self.edit(self.cam, name="Canon A-1")
        self.assertObjects("is neither")

    def test_a_source_that_is_not_a_url_is_caught(self):
        self.edit(self.cam, source="Wikipedia")
        self.assertObjects("https URL")

    def test_a_mount_with_no_record_is_caught(self):
        self.edit(self.cam, mount="nikon-f")
        self.assertObjects("no record in data/mount")

    def test_a_film_that_does_not_say_whether_it_is_discontinued_is_caught(self):
        self.edit(self.film, discontinued=None)
        self.assertObjects("whether it is discontinued")

    def test_discontinued_on_something_that_is_not_a_film_is_caught(self):
        self.edit(self.cam, discontinued=True)
        self.assertObjects("belongs to a film")

    def test_a_body_claiming_both_a_mount_and_a_fixed_lens_is_caught(self):
        self.edit(self.cam, lens="Canon 40mm")
        self.assertObjects("both a mount and a fixed lens")

    def test_an_alternate_that_shadows_a_record_is_caught(self):
        self.edit(self.lens, alternates=[{"brand": "nikon", "slug": "nikkor-45mm-f2-8e-ed"}])
        self.assertObjects("is already a record")

    def test_two_records_claiming_one_alternate_is_caught(self):
        write(os.path.join(self.root, "data/lens/nikon/nikkor-50mm-f1-8.json"),
              {"name": "Nikkor 50mm f/1.8", "brand": "Nikon",
               "alternates": [{"brand": "nikkor", "slug": "45mm-f2-8e-ed"}],
               "source": "https://en.wikipedia.org/wiki/Nikon_F-mount"})
        self.assertObjects("also claimed by")

    def test_a_malformed_alternate_is_caught(self):
        self.edit(self.lens, alternates=[{"brand": "nikkor"}])
        self.assertObjects("needs exactly a brand and a slug")

    def test_two_mounts_claiming_one_spelling_is_caught(self):
        write(os.path.join(self.root, "data/mount/canon-fl.json"),
              {"name": "Canon FL", "brand": "Canon", "spellings": ["Canon FD"]})
        self.assertObjects("already claimed by")

    def test_a_brand_that_collides_with_the_sites_own_paths_is_caught(self):
        write(os.path.join(self.root, "data/camera/support/x-1.json"),
              {"name": "Support X-1", "brand": "Support",
               "source": "https://en.wikipedia.org/wiki/X"})
        self.assertObjects("path the site already answers")

    def test_a_filename_that_is_not_a_slug_is_caught(self):
        os.rename(self.cam, os.path.join(os.path.dirname(self.cam), "AE_1.json"))
        self.assertObjects("is not a slug")


if __name__ == "__main__":
    unittest.main()
