"""The sheets and the redirect manifest, checked against the real corpus."""

import os
import re
import unittest

from build import redirects, sheets
from content import load, url_prefix
from validate import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Lenses whose name does not carry their brand: issue #42, frozen by slug so
# that resolving one and gaining another cannot cancel out. Only ever shrinks.
HELD = frozenset({
    "cosmicar-70-200mm-f4", "cpc-135mm-f2-8-mc-auto-a", "cpc-28-80mm-f3-5-4-5",
    "cpc-28-85mm-f3-5-4-5", "cpc-28mm-f2-8-auto-a", "eikor-28mm-f2-8",
    "eikor-80-200mm-f4-5", "focal-135mm-f2-8-mc-auto", "focal-28mm-f2-8-mc-auto",
    "gemini-28mm-f2-8", "hanimex-mc-80-200mm-f4-5", "hervic-zivnon-23mm-f3-5",
    "irix-11mm-f4-0-blackstone", "irix-11mm-f4-0-firefly", "irix-15mm-f2-4-blackstone",
    "irix-15mm-f2-4-firefly", "jc-penney-135mm-f2-8", "kiron-105mm-f2-8-macro",
    "kiron-24mm-f2-rl", "kiron-28-70mm-f4-macro", "kiron-28mm-f2",
    "laowa-105mm-f2-smooth-trans-focus", "laowa-12mm-f2-8-zero-d",
    "laowa-15mm-f4-wide-angle-macro", "laowa-25mm-f2-8-2-5-5x-ultra-macro",
    "laowa-60mm-f2-8-2x-ultra-macro", "lester-a-dine-kiron-105mm-f2-8-macro",
    "loreo-35mm-f11-22-shift-lens", "loreo-38mm-f11-3d-stereo", "luxon-50mm-f2-0-mc",
    "mc-apo-telezenitar-k-1-2-8-135mm-telephoto",
    "mc-apo-telezenitar-k-300mm-f4-5-2008-telephoto", "mc-cosmicar-28-80mm-f3-5-4-5",
    "mc-cosmicar-28mm-f2-8", "mc-helios-44k-4-58mm-f2", "mc-helios-77k-4-50mm-f1-8",
    "mc-variozenitar-k-1-3-5-4-5-35-105mm-zoom",
    "mc-variozenitar-k-1-4-0-70-210mm-zoom",
    "mc-variozenitar-k-25-45mm-f2-8-3-5-2008-zoom",
    "mc-variozenitar-k-35-100mm-f2-8-1980-zoom", "mc-zenitar-1-1-4-50mm",
    "mc-zenitar-1k-1-1-4-85mm-telephoto", "mc-zenitar-k-1-1-9-50mm",
    "mc-zenitar-k-1-2-8-20mm", "mc-zenitar-k-1-2-8-28mm", "mc-zenitar-k-16mm-f2-8",
    "mc-zenitar-k2-50mm-f2", "mir-20k-20mm-f3-5", "mir-47k-20mm-f2-5",
    "mitakon-28-200mm-f3-8-5-5", "mitakon-80-200mm-f4-5-mc-zoom",
    "oberon-11k-200mm-f2-8", "opteka-opt500mir-c-500mm-f8", "ozunon-35mm-75mm-f3-5-4-5",
    "panagor-e-pmc-auto-zoom-28mm-80mm-f3-5-4-5", "pcs-arsat-35mm-f2-8-shift",
    "peleng-8mm-f3-5", "phoenix-500mm-f8-reflex-catadioptric",
    "phoenix-800mm-f8-reflex-catadioptric", "polar-800mm-f8-reflex-catadioptric",
    "polar-85mm-portrait-lens-f1-4-aspherical-if", "porst-135mm-f2-8-tele-as-mc-e",
    "porst-200mm-f3-5", "porst-28mm-f2-8-mc-auto", "porst-40mm-f2-5-mc-auto",
    "porst-55mm-f1-2-mc-auto", "porst-55mm-f1-2-reflex-mc-auto", "porst-75-260mm-f4-5",
    "quantaray-af-100-300mm-f4-5-6-7-ldo", "revu-50mm-f1-2", "revue-28-50mm-f3-5-4-5",
    "revue-28-70mm-f3-5-4-5", "revue-35mm-f2-8", "revue-70-210mm-f4-5-af",
    "revue-80-200mm-f4-5", "revuenon-135mm-f2-8", "revuenon-200mm-f3-3",
    "revuenon-200mm-f3-5", "revuenon-300mm-f5-6", "revuenon-500mm-f8-0-mirror",
    "revuenon-55mm-f1-2", "revuenon-auto-45mm-f2-8", "revuenon-auto-mc-135mm-f2-8",
    "revuenon-auto-mc-28mm-f2-8", "revuenon-auto-mc-55mm-f1-4",
    "revuenon-auto-mc-55mm-f1-7", "revuenon-auto-multicoated-28mm-f2-8",
    "rokinon-500mm-f6-3-reflex", "sun-28-80mm-f3-5-4-5-macro",
    "sun-70-140mm-f3-8-auto-zoom", "sun-80-200mm-f4-5-macro",
    "sun-85-210mm-f4-8-telephoto-zoom", "sunagor-75-300mm-f5-6",
    "suntop-28-135mm-f3-8-5-2-mc", "takumar-135mm-f2-5-prime",
    "takumar-a-28-80mm-f3-5-4-5-macro", "tou-five-star-28-135mm-1-3-5-5-2-macro",
    "tou-five-star-28-80mm-1-3-5-4-5-macro", "tou-five-star-500mm-1-8",
    "tou-five-star-70-210mm-1-4-5-22-macro", "tou-five-star-75-200mm-1-4-5-macro",
    "tou-five-star-mc-auto-200mm-1-4-5", "tou-five-star-mc-auto-28mm-1-2-8-to-f22",
    "tou-five-star-mc-auto-35-75mm-1-3-5-4-8-macro",
    "toyo-five-star-mc-auto-28mm-1-2-8-to-f16", "volna-10k-35mm-f1-8",
    "volna-50mm-f1-8", "zenitar-mc-35mm-tilt-and-shift-f2-8",
    "zenitar-mc-80mm-tilt-and-shift-f2-8",
})
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
        """A lens name carries its brand, because a flat list has no directory.

        On this site the brand is the path, so `FD 100mm f/2` under
        `/lens/canon/` is unambiguous. Read as a list it is not: a person typing
        into a field, or reading an export, gets `FD 100mm f/2` with nothing
        saying Canon. Nikon's 275 lenses said Nikkor and never Nikon.

        The exception is listed rather than described, because it is a defect
        and not a style. 107 of the 109 came off `Pentax K-mount`, which lists
        **third-party** glass that fits K — Kiron, Revuenon, Porst, Laowa, the
        Zenit line — filed under the mount's brand because that is the article
        it was read from. Their `brand` is wrong today; prefixing would only
        state it out loud, and `Pentax Kiron 28-70mm f4 Macro` is a lens that
        never existed. The other two, `Takumar 135mm f2.5 prime` and `Takumar A
        28-80mm`, are genuinely Pentax and want only their name fixed. Both
        kinds are in `HELD` and both are in issue #42.

        The set is frozen by slug rather than counted. A count passes if one
        record is resolved and another arrives unbranded in the same change,
        and #42 resolves these one at a time across many pull requests, which
        is exactly when that trade would go unnoticed.
        """
        def tokens(value):
            # Split the way the slug does. `Schneider-Kreuznach D-Xenogon` is
            # two words of the brand written with a hyphen, and splitting on
            # whitespace alone reads it as neither.
            return {w for w in re.split(r"[^0-9a-z]+", value.casefold()) if w}

        held = {}
        for e in sheets(ROOT)["lens"]["entries"]:
            if tokens(e["brand"]) <= tokens(e["name"]):
                continue
            held[e["slug"]] = e
            if e["brand"] != "Pentax":
                self.fail(f"{e['name']!r} is a {e['brand']} and does not say so — "
                          "a lens name carries its brand")
        arrived = sorted(set(held) - HELD)
        self.assertEqual(arrived, [], f"{arrived} has no brand in its name, and "
                         "a new one may not join the held set")
        resolved = sorted(HELD - set(held))
        self.assertEqual(resolved, [], f"{resolved} left the held set; that is the "
                         "point of #42, so take it out of HELD in the same change")

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
