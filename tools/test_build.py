"""The sheets and the redirect manifest, checked against the real corpus."""

import os
import re
import unittest

from build import redirects, sheets
from content import load, url_prefix
from validate import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Build(unittest.TestCase):
    def test_the_real_corpus_validates(self):
        self.assertEqual(validate(ROOT), [])

    def test_every_entry_carries_the_url_it_will_be_served_at(self):
        for kind, sheet in sheets(ROOT).items():
            self.assertTrue(sheet["entries"], f"{kind} is empty")
            prefix = url_prefix(ROOT)
            for e in sheet["entries"]:
                self.assertTrue(e["url"].startswith(f"{prefix}/{kind}/"), e["url"])
                # No dots: the site's router reads one as a file extension and
                # never appends /index.html. See tools/slug.py.
                self.assertNotIn(".", e["url"])

    def test_every_sheet_carries_its_licence(self):
        for kind, sheet in sheets(ROOT).items():
            self.assertEqual(sheet["license"], "CC-BY-SA-4.0")
            self.assertIn("Wikipedia", sheet["attribution"])

    def test_a_name_and_its_edition_identify_one_record(self):
        """A consumer can tell two records apart without fetching either.

        A sheet is read as a flat list — the app puts these names in a field a
        person types into — so two entries that print the same string are two
        entries nobody can choose between. Thirty lens titles here name two
        products, and `variant` is the whole difference: the slug carries it
        (`validate.py` refuses one that does not) but a slug is an address, and
        a person picking a lens is not reading addresses.

        `name` alone is therefore *not* the identity and asserting it were would
        fail against the real corpus. The pair is, everywhere, in all four
        sheets.
        """
        for kind, sheet in sheets(ROOT).items():
            seen = {}
            for e in sheet["entries"]:
                key = (e.get("name", e.get("title")), e.get("variant"))
                # Not `assertNotIn`: it prints the container, and the container
                # is every entry in the sheet. The two slugs are the answer.
                if key in seen:
                    self.fail(f"{kind}: {key[0]!r} is both {seen[key]} and "
                              f"{e['slug']} — two records a consumer would "
                              "print identically")
                seen[key] = e["slug"]

    def test_a_lens_name_says_whose_shelf_it_came_off(self):
        """Every lens name carries its brand, because a flat list has no directory.

        On this site the brand is the path, so `FD 100mm f/2` under
        `/lens/canon/` is unambiguous. Read as a list it is not: a person typing
        into a field, or reading an export, gets `FD 100mm f/2` with nothing
        saying Canon. Nikon's 275 lenses said Nikkor and never Nikon.

        This held 109 exceptions for two releases, all of them lenses filed
        under Pentax that Pentax never sold — the mount's brand, taken from the
        article they were read from. Issue #42 moved them onto the shelf of
        whoever sold each one, so the exception list is gone and the rule is
        now unconditional. A record that cannot satisfy it has a `brand` that
        is wrong, which is what the 109 turned out to be.
        """
        def tokens(value):
            # Split the way the slug does. `Schneider-Kreuznach D-Xenogon` is
            # two words of the brand written with a hyphen, and splitting on
            # whitespace alone reads it as neither.
            return {w for w in re.split(r"[^0-9a-z]+", value.casefold()) if w}

        missing = [f"{e['brand']} / {e['name']}"
                   for e in sheets(ROOT)["lens"]["entries"]
                   if not tokens(e["brand"]) <= tokens(e["name"])]
        self.assertEqual(missing, [], "a lens name carries its brand; if this one "
                         "cannot, check whether its brand is the seller or only "
                         "the mount it fits")

    # A body whose brand is not its mount's, and the reason each is allowed.
    # Every one of these is a maker building to a standard someone else set,
    # which is a real and ordinary thing; what is not real is a body joined to
    # a mount because the mount's *name* contained the string the importer had.
    OTHER_MAKERS_MOUNTS = {
        ("Leitz Minolta CL", "leica-m"),   # Leitz and Minolta built it together
        ("Minolta CLE", "leica-m"),        # Minolta's own M-mount rangefinder
        ("Canon VT", "leica-m39"),         # Canon's rangefinders took LTM glass
        ("Canon 7", "leica-m39"),
        ("Canon P", "leica-m39"),
        ("Ricoh XR-1", "pentax-k"),        # the K mount was licensed widely
    }

    def test_a_body_wears_another_maker_s_mount_only_on_the_record(self):
        """A camera joined to a mount no one at that company designed.

        Six of these are true: Leitz and Minolta built the CL together, Canon's
        rangefinders took Leica screw glass, Ricoh licensed the K. The seventh
        was not. The Canonflex was filed under `leica-r` because its infobox
        says `[[R mount]]` — a redlink — and `leica-r` claimed the bare
        spelling `R mount`. Canon's own R mount is a breech-lock of 1959 that
        became the FL; the two share a letter and nothing else. The spelling is
        now claimed by neither, so the next importer gets no answer instead of
        a confident wrong one.

        A mount is the one field on a body that cannot be checked against its
        name, so a wrong one is invisible: the record reads fine and joins the
        body to a shelf of glass that will not fit it. This list is short
        enough to read, which is the point — a new entry is a claim that some
        maker built to another's standard, and it gets made here, in a file
        someone reviews, rather than inside an importer nobody re-reads.

        Third-party glass is the opposite case and is not tested: 423 lenses
        here carry another maker's mount, because being built to fit someone
        else's camera is what a third-party lens is.
        """
        # From the records, not the sheets: the sheets carry no `mount`, and
        # deliberately so — the app fills a name field and joins nothing.
        records, mounts, _ = load(ROOT)
        brand_of = {slug: meta.get("brand") for slug, meta in mounts.items()}
        crossed = {(r.meta["title"], m)
                   for r in records if r.kind == "camera"
                   for m in (r.meta.get("mount") or [])
                   if brand_of.get(m) and brand_of[m] != r.meta.get("brand")}
        self.assertEqual(crossed - self.OTHER_MAKERS_MOUNTS, set(),
                         "a body on another maker's mount: confirm the maker "
                         "built to that standard, then name it above")
        self.assertEqual(self.OTHER_MAKERS_MOUNTS - crossed, set(),
                         "an exception no record needs any more")

    def test_the_editions_the_source_distinguishes_survive_the_sheet(self):
        """The thirty collisions, by name, rather than only in the aggregate.

        A sheet that dropped `variant` still passes the pair test above by
        accident on any corpus where no two titles collide, and this corpus is
        one edit away from being that. So one real pair is named: both barrels
        of a lens the source lists twice, distinguishable, from one sheet.
        """
        lenses = [e for e in sheets(ROOT)["lens"]["entries"]
                  if e["name"] == "Canon FD 100mm f/2.8"]
        self.assertEqual(len(lenses), 2, "the source lists both barrels")
        self.assertEqual({e.get("variant") for e in lenses}, {None, "New FD"})

    def test_a_derived_figure_equals_the_mount_it_was_derived_from(self):
        """`derived` means the number was never stated of this mount.

        `pentax-kf` and `ricoh-rk` are the Pentax K plus five contacts and one
        pin; `canon-r` shares the FD's flange because `Canon R lens mount` says
        the lugs, flange focal distance and breech-lock ring are mutually
        compatible. Nothing states 45.46 mm of the K-F or 42 mm of the R, so
        the figures are inherited — and an inherited figure that stops matching
        its parent is either a corrected parent nobody propagated or a claim
        that quietly became original.
        """
        _, mounts, _ = load(ROOT)
        for child, parent in (("pentax-kf", "pentax-k"),
                              ("ricoh-rk", "pentax-k"),
                              ("canon-r", "canon-fd")):
            for field in ("flange", "throat", "tabs"):
                if field not in mounts[child]:
                    continue
                self.assertEqual(
                    mounts[child][field], mounts[parent].get(field),
                    f"{child}.{field} is derived from {parent} and no longer "
                    "matches it; either propagate the correction or give "
                    f"{child} a source of its own")
                self.assertEqual(mounts[child]["measured"][field], "derived")

    def test_the_two_mamiya_67_mounts_are_what_the_split_claimed(self):
        """The split is only justified by the numbers that differ.

        `mamiya-breech-lock` held the RB67 and the RZ67 because both articles
        use the identical phrase "Custom Mamiya breech-lock bayonet mount".
        Splitting them says that phrase names a family, and the evidence is two
        flange distances stated on two pages. If those ever agree, the split
        has no basis left and the records should be one again.
        """
        _, mounts, _ = load(ROOT)
        rb, rz = mounts["mamiya-rb67"], mounts["mamiya-rz67"]
        self.assertNotEqual(rb["flange"], rz["flange"])
        self.assertEqual((rb["flange"], rz["flange"]), (110.0, 105.0))
        for m in (rb, rz):
            # Not the list's "Bayonet": both bodies' own pages say breech-lock,
            # and the list is the source that also says the RB is 112 mm.
            self.assertEqual(m["measured"]["flange"], "article")
            self.assertEqual(m["type"], "Breech-lock bayonet")

    def test_no_image_reaches_the_sheets(self):
        """The sheets are what the app bundles, and images do not go in it.

        A vendor's product photograph is used here under fair use, which is a
        use and not a licence: it cannot be sublicensed, and every sheet
        declares itself CC-BY-SA-4.0. Compiling those images into a shipped
        application is also a materially weaker position than showing them on a
        reference page, and the app has no need of them — it fills a name field.

        So the sheets carry names and URLs and nothing about a file in a bundle.
        That is true today by construction rather than by intent, which is
        exactly the kind of thing that stops being true quietly.
        """
        import json
        for kind, sheet in sheets(ROOT).items():
            blob = json.dumps(sheet)
            for token in ("resources", "credit", "sourcePage", "fair-use",
                          ".png", ".jpg", ".jpeg", ".webp"):
                self.assertNotIn(token, blob,
                                 f"{kind}.json carries image data: {token!r}")


class Redirects(unittest.TestCase):
    def setUp(self):
        self.r = redirects(ROOT)
        self.records = {x.url: x for x in load(ROOT)[0]}

    def test_a_provisional_redirect_points_at_its_own_row_in_its_brand_list(self):
        for row in self.r["provisional"]:
            self.assertEqual(row["to"], self.records[row["from"]].list_url)

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
