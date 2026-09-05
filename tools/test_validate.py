"""Each guard, mutated until it fails.

A guard no test can break is a guard nobody can prove. Every test starts from a
fixture that validates cleanly, makes one change, and asserts that the named
rule — not merely *some* rule — objects.
"""

import datetime
import os
import shutil
import tempfile
import unittest

from content import load
from validate import STALE_AFTER_DAYS, validate


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
        self.hugo_toml = os.path.join(self.root, "hugo.toml")
        with open(self.hugo_toml, "w", encoding="utf-8") as fh:
            fh.write('baseURL = "https://example.test/library/"\n')
        c = os.path.join(self.root, "content")
        # A brand is a shelf and needs its own page, which is where its other
        # names live.
        page(f"{c}/camera/canon/_index.md", 'title = "Canon"')
        page(f"{c}/film/kodak/_index.md", 'title = "Kodak"')
        page(f"{c}/lens/nikon/_index.md", 'title = "Nikon"')
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
             'aliases = ["/lens/nikkor/45mm-f2-8e-ed/"]')
        self.cam = f"{c}/camera/canon/ae-1/index.md"
        self.film = f"{c}/film/kodak/portra-400/index.md"
        self.lens = f"{c}/lens/nikon/nikkor-45mm-f2-8e-ed/index.md"
        self.content = c
        self.brand = f"{c}/camera/canon/_index.md"

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
        self.assertObjects("is none of")

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

    def test_an_alias_that_shadows_a_record_is_caught(self):
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                'aliases = ["/lens/nikon/nikkor-45mm-f2-8e-ed/"]')
        self.assertObjects("is already a record")

    def test_two_records_claiming_one_alias_is_caught(self):
        page(f"{self.content}/lens/nikon/nikkor-50mm-f1-8/index.md",
             'title = "Nikkor 50mm f/1.8"\nbrand = "Nikon"\n'
             'source = "https://x.example/a"\n'
             'aliases = ["/lens/nikkor/45mm-f2-8e-ed/"]')
        self.assertObjects("also claimed by")

    def test_a_malformed_alias_is_caught(self):
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                'aliases = ["/lens/nikkor"]')
        self.assertObjects("is not /<kind>/<brand>/<slug>/")

    def test_an_alias_filed_under_the_wrong_kind_is_caught(self):
        # A camera reached at a lens address is a redirect between two things
        # that are not the same kind of thing.
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                'aliases = ["/camera/nikkor/45mm-f2-8e-ed/"]')
        self.assertObjects("is filed under")

    def test_an_alias_with_a_bad_segment_is_caught(self):
        self.rewrite(self.lens, 'title = "Nikkor 45mm f/2.8E ED"\nbrand = "Nikon"\n'
                                'source = "https://x.example/a"\n'
                                'aliases = ["/lens/Nikkor/45mm_F2.8/"]')
        self.assertObjects("not a slug")

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


class BrandPages(Fixture):
    """A brand is a shelf, and a shelf can have had more than one name.

    `Svema (Astrum)` is Svema film made by its successor company; `AgfaPhoto`
    and `Agfa-Gevaert` are corporate lineage rather than a different shelf.
    Someone looking for any of those names is looking for one place, so the
    other names are aliases on the brand's own page.
    """

    def test_a_brand_with_no_page_is_caught(self):
        os.remove(self.brand)
        self.assertObjects("no _index.md")

    def test_a_brand_title_that_does_not_match_its_directory_is_caught(self):
        page(self.brand, 'title = "Canon Inc."')
        self.assertObjects("not 'canon'")

    def test_a_brand_alias_that_shadows_a_real_brand_is_caught(self):
        page(self.brand, 'title = "Canon"\naliases = ["/camera/canon/"]')
        self.assertObjects("is already a brand")

    def test_two_brands_claiming_one_alias_is_caught(self):
        page(self.brand, 'title = "Canon"\naliases = ["/camera/canonet/"]')
        page(f"{self.content}/camera/nikon/_index.md",
             'title = "Nikon"\naliases = ["/camera/canonet/"]')
        page(f"{self.content}/camera/nikon/fm2/index.md",
             'title = "Nikon FM2"\nbrand = "Nikon"\nsource = "https://x.example/a"')
        self.assertObjects("also claimed by")

    def test_a_brand_alias_of_the_wrong_shape_is_caught(self):
        page(self.brand, 'title = "Canon"\naliases = ["/camera/canonet/g-iii/"]')
        self.assertObjects("is not /<kind>/<brand>/")

    def test_a_brand_alias_under_another_kind_is_caught(self):
        page(self.brand, 'title = "Canon"\naliases = ["/lens/canonet/"]')
        self.assertObjects("is filed under")

    def test_an_unknown_field_on_a_brand_page_is_caught(self):
        page(self.brand, 'title = "Canon"\nfounded = 1937')
        self.assertObjects("unknown field")

    def test_a_well_formed_brand_alias_is_accepted(self):
        page(self.brand, 'title = "Canon"\naliases = ["/camera/canonet/", "/camera/kwanon/"]')
        self.assertEqual(validate(self.root), [])


class Variants(Fixture):
    """An edition of a product, where the product's own name does not name it.

    Canon's second-generation FD lenses say only `FD` on the barrel; `New FD` is
    Canon's word for the edition. Hasselblad's C/CF/CFi/CFE barrels are the same
    shape. Two records can therefore share a title, which means the slug has to
    carry the variant or they would share an address too.
    """

    def variant_page(self, slug, variant, title="Canon AE-1 Lens"):
        page(f"{self.content}/lens/nikon/{slug}/index.md",
             f'title = "{title}"\nbrand = "Nikon"\n'
             f'variant = "{variant}"\nsource = "https://x.example/a"')

    def test_two_editions_of_one_title_are_accepted(self):
        page(f"{self.content}/lens/nikon/50mm-f1-4/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nsource = "https://x.example/a"')
        page(f"{self.content}/lens/nikon/50mm-f1-4-ai-s/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nvariant = "AI-S"\n'
             'source = "https://x.example/a"')
        self.assertEqual(validate(self.root), [])

    def test_a_slug_that_does_not_carry_the_variant_is_caught(self):
        # Without this, the second edition wants the first one's address.
        page(f"{self.content}/lens/nikon/50mm-f1-4/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nvariant = "AI-S"\n'
             'source = "https://x.example/a"')
        self.assertObjects("does not carry the variant")

    def test_an_empty_variant_is_caught(self):
        page(f"{self.content}/lens/nikon/50mm-f1-4-ai-s/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nvariant = "  "\n'
             'source = "https://x.example/a"')
        self.assertObjects("variant must be a non-empty string")

    def test_a_variant_that_is_not_a_string_is_caught(self):
        page(f"{self.content}/lens/nikon/50mm-f1-4-2/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nvariant = 2\n'
             'source = "https://x.example/a"')
        self.assertObjects("variant must be a non-empty string")

    def test_a_record_without_a_variant_still_takes_the_plain_slug(self):
        page(f"{self.content}/lens/nikon/50mm-f1-4/index.md",
             'title = "50mm f/1.4"\nbrand = "Nikon"\nsource = "https://x.example/a"')
        self.assertEqual(validate(self.root), [])


class Photographs(Fixture):
    """A photograph is the one thing here that can put someone in breach.

    174 of the 201 camera images on Wikipedia require credit by name, and two of
    them are local en.wiki uploads — which is where non-free fair-use files live,
    and they look identical to the free ones from the article side. So the credit
    is required data rather than a convention, and the licence is checked.
    """

    GOOD = (f'title = "Canon AE-1"\nbrand = "Canon"\n'
            'source = "https://en.wikipedia.org/wiki/Canon_AE-1"\n'
            '\n[[resources]]\nsrc = "ae-1.jpg"\n[resources.params]\n'
            'credit = "Groogle"\nlicense = "CC BY-SA 4.0"\n'
            'licenseUrl = "https://creativecommons.org/licenses/by-sa/4.0/"\n'
            'alt = "A black Canon AE-1 seen from the front"\n'
            'sourcePage = "https://commons.wikimedia.org/wiki/File:Canon_AE-1.jpg"\n'
            f'verified = "{datetime.date.today().isoformat()}"')

    def with_image(self, front=None):
        open(os.path.join(os.path.dirname(self.cam), "ae-1.jpg"), "wb").close()
        self.rewrite(self.cam, front if front is not None else self.GOOD)

    def test_a_fully_credited_photograph_is_accepted(self):
        self.with_image()
        self.assertEqual(validate(self.root), [])

    def test_an_image_with_no_resources_entry_is_caught(self):
        self.with_image('title = "Canon AE-1"\nbrand = "Canon"\n'
                        'source = "https://x.example/a"')
        self.assertObjects("ships with no credit and no licence")

    def test_each_required_credit_field_is_caught_when_missing(self):
        for field in ("credit", "license", "licenseUrl", "alt", "sourcePage"):
            with self.subTest(field=field):
                front = "\n".join(l for l in self.GOOD.split("\n")
                                  if not l.startswith(f"{field} = "))
                self.with_image(front)
                self.assertObjects(f"has no {field}")

    def test_a_non_free_licence_is_refused(self):
        self.with_image(self.GOOD.replace('license = "CC BY-SA 4.0"',
                                          'license = "Fair use"'))
        self.assertObjects("not a licence this repository can redistribute")

    def test_a_non_commercial_licence_is_refused(self):
        # The allowlist matches by prefix so "CC BY-SA 3.0 de" works without
        # enumerating every port, and that same prefix makes "CC BY-NC 2.0"
        # start with "cc by". These pages support a paid application, so the
        # breach would be the publisher's rather than a later contributor's.
        for lic in ("CC BY-NC 2.0", "CC BY-NC-SA 3.0", "CC BY-NC-ND 4.0"):
            with self.subTest(licence=lic):
                self.with_image(self.GOOD.replace('license = "CC BY-SA 4.0"',
                                                  f'license = "{lic}"'))
                self.assertObjects("not a licence this repository can redistribute")

    def test_no_derivatives_is_accepted(self):
        # ND was refused here once, for two reasons that were both wrong: that
        # Hugo's resize makes a derivative (CC 4.0 2(a)(4) says the technical
        # modifications needed to serve a work never produce Adapted Material,
        # and `.Fit` does not crop), and that a contributor might crop one (so
        # might they crop a CC BY-SA file, and nothing here detects either).
        # The corpus already carries fair-use vendor photographs, which grant a
        # reuser nothing; ND grants commercial use and verbatim redistribution.
        self.with_image(self.GOOD.replace('license = "CC BY-SA 4.0"',
                                          'license = "CC BY-ND 4.0"'))
        self.assertEqual(validate(self.root), [])

    def test_a_source_page_that_is_not_a_url_is_caught(self):
        self.with_image(self.GOOD.replace(
            'sourcePage = "https://commons.wikimedia.org/wiki/File:Canon_AE-1.jpg"',
            'sourcePage = "Commons"'))
        self.assertObjects("sourcePage must be an https URL")

    def test_a_resources_entry_for_a_file_that_is_not_there_is_caught(self):
        # Credit for a photograph nobody can see is credit nobody can check.
        self.rewrite(self.cam, self.GOOD)
        self.assertObjects("which is not in the bundle")

    def test_a_resource_without_a_src_is_caught(self):
        self.with_image(self.GOOD.replace('src = "ae-1.jpg"\n', ""))
        self.assertObjects("needs a src")


class UrlPrefix(Fixture):
    """Hugo is the authority on what a URL is; the Python only asserts it."""

    def urls(self):
        return {r.url for r in load(self.root)[0]}

    def test_urls_carry_the_prefix_hugo_serves_under(self):
        self.assertIn("/library/camera/canon/ae-1", self.urls())

    def test_moving_the_baseurl_moves_every_url(self):
        # The regression this exists for: a hardcoded "/library" in the Python
        # would keep emitting the old prefix while Hugo followed the new one, and
        # nothing would say so.
        with open(self.hugo_toml, "w", encoding="utf-8") as fh:
            fh.write('baseURL = "https://example.test/gear/"\n')
        self.assertIn("/gear/camera/canon/ae-1", self.urls())
        self.assertNotIn("/library/camera/canon/ae-1", self.urls())

    def test_a_baseurl_with_no_path_yields_root_relative_urls(self):
        with open(self.hugo_toml, "w", encoding="utf-8") as fh:
            fh.write('baseURL = "https://example.test/"\n')
        self.assertIn("/camera/canon/ae-1", self.urls())


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

    def test_an_image_promotes_but_does_not_excuse_itself_from_credit(self):
        # Promotion and licensing are separate questions, and the second one is
        # the one that can put someone in breach.
        open(os.path.join(os.path.dirname(self.cam), "ae-1.jpg"), "wb").close()
        self.assertIn("ae-1", self.promoted())
        self.assertObjects("ships with no credit and no licence")

    def test_a_note_promotes_a_record(self):
        # A ruling nobody can read is not documentation. Before this, the note
        # explaining that the Agfa K-mount lens is a rebadged Chinon existed and
        # was unreachable, because its record had no page.
        self.rewrite(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                               'source = "https://x.example/a"\n'
                               'note = "Sold as the AE-1 Program in some markets."')
        self.assertIn("ae-1", self.promoted())

    def test_a_non_image_file_does_not_promote_a_record(self):
        open(os.path.join(os.path.dirname(self.cam), "notes.txt"), "wb").close()
        self.assertEqual(self.promoted(), set())


if __name__ == "__main__":
    unittest.main()


class FairUse(Fixture):
    """A vendor's own photograph of a box, which no free licence can reach.

    The box is a graphic work and the whole subject, so a photograph of one has
    two owners and a contributor can license only their half. The maker's own
    shot has one owner — so it is admitted, and admitted as a *use* rather than
    a licence, with the holder named where a licenceUrl would be meaningless.
    """

    def setUp(self):
        super().setUp()
        self.cam = os.path.join(self.root, "content/camera/canon/ae-1/index.md")
        open(os.path.join(os.path.dirname(self.cam), "ae-1.jpg"), "wb").close()

    def declare(self, **over):
        params = {"credit": "Canon Inc.", "license": "fair-use",
                  "copyright": "Canon Inc.", "alt": "A boxed Canon AE-1",
                  "sourcePage": "https://canon.example/ae-1",
                  "verified": datetime.date.today().isoformat(), **over}
        body = "".join(f'    {k} = "{v}"\n' for k, v in params.items() if v is not None)
        page(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                       'source = "https://x.example/a"\n\n[[resources]]\n'
                       f'  src = "ae-1.jpg"\n  [resources.params]\n{body}'.rstrip("\n"))
        return " ".join(validate(self.root))

    def test_a_vendor_image_validates(self):
        self.assertEqual(self.declare(), "")

    def test_it_must_name_the_holder(self):
        self.assertIn("has no copyright", self.declare(copyright=None))

    def test_a_licenceUrl_says_nothing_true_about_a_fair_use_file(self):
        # There are no terms to link to, so carrying a link to some is a claim
        # that is not merely redundant but false.
        self.assertIn("carries a licenseUrl", self.declare(licenseUrl="https://x.example/"))

    def test_a_free_licence_still_may_not_name_a_holder_instead_of_terms(self):
        self.assertIn("carries a copyright",
                      self.declare(license="CC BY-SA 4.0",
                                   licenseUrl="https://creativecommons.org/licenses/by-sa/4.0/"))

    def test_anything_else_non_free_is_still_refused(self):
        self.assertIn("not a licence this repository can redistribute",
                      self.declare(license="all rights reserved",
                                   licenseUrl="https://x.example/", copyright=None))


class Freshness(Fixture):
    """When someone last confirmed the credit is still true.

    Every other field on an image describes the day it arrived. This is the only
    one that can stop being true without a commit — a `sourcePage` is a URL and
    URLs die, and Commons deletes files for exactly the licensing reasons this
    scheme is about. A photograph whose credit has been withdrawn at the source
    looks identical to one that has not.
    """

    def setUp(self):
        super().setUp()
        self.cam = os.path.join(self.root, "content/camera/canon/ae-1/index.md")
        open(os.path.join(os.path.dirname(self.cam), "ae-1.jpg"), "wb").close()

    def on(self, when):
        params = {"credit": "Rpvdk", "license": "Public domain",
                  "licenseUrl": "https://commons.example/l", "alt": "A Canon AE-1",
                  "sourcePage": "https://commons.example/File:x.jpg", "verified": when}
        body = "".join(f'{k} = "{v}"\n' for k, v in params.items() if v is not None)
        page(self.cam, 'title = "Canon AE-1"\nbrand = "Canon"\n'
                       'source = "https://x.example/a"\n\n[[resources]]\n'
                       f'src = "ae-1.jpg"\n[resources.params]\n{body}'.rstrip("\n"))
        return " ".join(validate(self.root))

    def days_ago(self, n):
        return (datetime.date.today() - datetime.timedelta(days=n)).isoformat()

    def test_a_claim_checked_today_passes(self):
        self.assertEqual(self.on(datetime.date.today().isoformat()), "")

    def test_a_claim_nobody_has_confirmed_is_refused(self):
        self.assertIn("has no verified", self.on(None))

    def test_a_date_that_is_not_a_date_is_refused(self):
        self.assertIn("is not a date", self.on("last tuesday"))

    def test_a_claim_verified_in_the_future_did_not_happen(self):
        self.assertIn("has not happened", self.on(self.days_ago(-2)))

    def test_a_claim_goes_stale_and_says_what_to_do_about_it(self):
        problem = self.on(self.days_ago(STALE_AFTER_DAYS + 40))
        self.assertIn("have not been re-verified", problem)
        self.assertIn("move the `verified` dates", problem)

    def test_it_is_still_fresh_the_day_before(self):
        # The boundary, so the threshold is the number it says it is.
        self.assertEqual(self.on(self.days_ago(STALE_AFTER_DAYS)), "")
