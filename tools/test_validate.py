"""Each guard, mutated until it fails.

A guard no test can break is a guard nobody can prove. Every test starts from a
fixture that validates cleanly, makes one change, and asserts that the named
rule — not merely *some* rule — objects.
"""

import os
import shutil
import tempfile
import unittest

from content import load
from validate import validate


def page(path, front, body=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("+++\n" + front.strip() + "\n+++\n")
        if body:
            fh.write("\n" + body + "\n")


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        c = os.path.join(self.root, "content")
        page(f"{c}/mount/canon-fd/_index.md",
             'title = "Canon FD"\nbrand = "Canon"\nspellings = ["Canon FD"]')
        page(f"{c}/mount/m42/_index.md",
             'title = "M42"\nspellings = ["M42 screw mount"]')
        page(f"{c}/camera/canon/ae-1/index.md",
             'title = "Canon AE-1"\nbrand = "Canon"\n'
             'source = "https://en.wikipedia.org/wiki/Canon_AE-1"\nmount = ["canon-fd"]')
        page(f"{c}/camera/canon/trip-35/index.md",
             'title = "Canon Trip 35"\nbrand = "Canon"\n'
             'source = "https://en.wikipedia.org/wiki/Canon_Trip"\nfixed_lens = "Zuiko 40mm"')
        page(f"{c}/film/kodak/portra-400/index.md",
             'title = "Kodak Portra 400"\nbrand = "Kodak"\ndiscontinued = false\n'
             'source = "https://en.wikipedia.org/wiki/List_of_photographic_films#Kodak"')
        page(f"{c}/lens/nikon/nikkor-45mm-f2-8e-ed/index.md",
             'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
             'source = "https://en.wikipedia.org/wiki/Nikon_F-mount"\n'
             '\n[[alternates]]\nbrand = "nikkor"\nslug = "45mm-f2-8e-ed"')
        self.cam = f"{c}/camera/canon/ae-1/index.md"
        self.film = f"{c}/film/kodak/portra-400/index.md"
        self.lens = f"{c}/lens/nikon/nikkor-45mm-f2-8e-ed/index.md"
        self.content = c

    def rewrite(self, path, front, body=""):
        page(path, front, body)

    def assertObjects(self, needle):
        problems = validate(self.root)
        self.assertTrue(any(needle in p for p in problems),
                        f"nothing objected to {needle!r}; got {problems}")


class Corpus(Fixture):
    # Without this every test below could be passing for the wrong reason.
    def test_the_fixture_itself_is_clean(self):
        self.assertEqual(validate(self.root), [])

    def test_front_matter_that_is_not_toml_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1\nbrand = ')
        self.assertObjects("not valid TOML")

    def test_a_file_with_no_front_matter_is_caught(self):
        with open(self.cam, "w", encoding="utf-8") as fh:
            fh.write("# Canon AE-1\n")
        self.assertObjects("no TOML front matter")

    def test_unclosed_front_matter_is_caught(self):
        with open(self.cam, "w", encoding="utf-8") as fh:
            fh.write('+++\ntitle = "Canon AE-1"\n')
        self.assertObjects("never closed")

    def test_a_missing_title_is_caught(self):
        self.rewrite(self.cam, 'brand = "Canon"\nsource = "https://x.example/a"')
        self.assertObjects("title is required")

    def test_an_unknown_field_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\niso = 400')
        self.assertObjects("unknown field")

    def test_a_brand_that_disagrees_with_its_directory_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Nikon"\n'
                               'source = "https://x.example/a"')
        self.assertObjects("not 'canon'")

    def test_a_slug_that_does_not_follow_from_the_title_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon A-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"')
        self.assertObjects("is neither")

    def test_a_source_that_is_not_a_url_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\nsource = "Wikipedia"')
        self.assertObjects("https URL")

    def test_a_mount_with_no_term_page_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\nmount = ["nikon-f"]')
        self.assertObjects("no term page")

    def test_a_mount_that_is_not_a_list_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\nmount = "canon-fd"')
        self.assertObjects("list of mount slugs")

    def test_a_film_that_does_not_say_whether_it_is_discontinued_is_caught(self):
        self.rewrite(self.film, 'title = "Kodak Portra 400"\nbrand = "Kodak"\n'
                                'source = "https://x.example/a"')
        self.assertObjects("whether it is discontinued")

    def test_discontinued_on_something_that_is_not_a_film_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\ndiscontinued = true')
        self.assertObjects("belongs to a film")

    def test_a_body_claiming_both_a_mount_and_a_fixed_lens_is_caught(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\nmount = ["canon-fd"]\n'
                               'fixed_lens = "Canon 40mm"')
        self.assertObjects("both a mount and a fixed lens")

    def test_an_alternate_that_shadows_a_record_is_caught(self):
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                '\n[[alternates]]\nbrand = "nikon"\nslug = "nikkor-45mm-f2-8e-ed"')
        self.assertObjects("is already a record")

    def test_two_records_claiming_one_alternate_is_caught(self):
        page(f"{self.content}/lens/nikon/nikkor-50mm-f1-8/index.md",
             'title = "Nikkor 50mm f/1.8"\nbrand = "Nikon"\n'
             'source = "https://x.example/a"\n'
             '\n[[alternates]]\nbrand = "nikkor"\nslug = "45mm-f2-8e-ed"')
        self.assertObjects("also claimed by")

    def test_a_malformed_alternate_is_caught(self):
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                '\n[[alternates]]\nbrand = "nikkor"')
        self.assertObjects("needs exactly a brand and a slug")

    def test_two_mounts_claiming_one_spelling_is_caught(self):
        page(f"{self.content}/mount/canon-fl/_index.md",
             'title = "Canon FL"\nbrand = "Canon"\nspellings = ["Canon FD"]')
        self.assertObjects("already claimed by")

    def test_a_brand_that_collides_with_the_sites_own_paths_is_caught(self):
        page(f"{self.content}/camera/support/x-1/index.md",
             'title = "Support X-1"\nbrand = "Support"\nsource = "https://x.example/a"')
        self.assertObjects("path the site already answers")

    # Casey's rule, and the reason it is a rule: an empty directory beside a
    # record invites someone to drop a photograph into it. A bare file does not,
    # and promoting one to a bundle later is as disruptive as this conversion was.
    def test_a_bare_markdown_file_instead_of_a_bundle_is_caught(self):
        page(f"{self.content}/camera/canon/a-1.md",
             'title = "Canon A-1"\nbrand = "Canon"\nsource = "https://x.example/a"')
        self.assertObjects("never a bare file")

    def test_a_bundle_with_no_index_is_caught(self):
        os.makedirs(f"{self.content}/camera/canon/f-1", exist_ok=True)
        self.assertObjects("no index.md")


class Promotion(Fixture):
    """A record earns its own page by having something to show, and nothing else."""

    def promoted(self):
        records, _, _ = load(self.root)
        return {r.slug for r in records if r.promoted}

    def test_a_record_with_nothing_to_show_is_not_promoted(self):
        self.assertEqual(self.promoted(), set())

    def test_prose_promotes_a_record(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"',
                     "The first camera Canon sold in real volume.")
        self.assertIn("ae-1", self.promoted())

    def test_whitespace_is_not_prose(self):
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"', "   \n\t\n")
        self.assertEqual(self.promoted(), set())

    def test_an_image_in_the_bundle_promotes_a_record(self):
        open(os.path.join(os.path.dirname(self.cam), "ae-1.jpg"), "wb").close()
        self.assertIn("ae-1", self.promoted())
        # And the corpus still validates: a photograph is not front matter.
        self.assertEqual(validate(self.root), [])

    def test_a_non_image_file_does_not_promote_a_record(self):
        open(os.path.join(os.path.dirname(self.cam), "notes.txt"), "wb").close()
        self.assertEqual(self.promoted(), set())


if __name__ == "__main__":
    unittest.main()
