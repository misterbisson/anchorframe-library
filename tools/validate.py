"""The check that stands between a pull request and the corpus.

The extraction that seeded this repository is not something anyone re-runs on a
schedule: it took judgement, and reproducing it would take more. So the files in
`content/` are the source of truth rather than an output, they are edited by
hand, and this is what makes a hand edit safe to accept by reading its diff
instead of the whole corpus.

Hugo will render a page with a missing brand, a mount nothing defines, or a
slug that has nothing to do with its title. Hugo has no opinion about any of
that. This does.

Every rule is mutation-tested in `test_validate.py`: a guard no test can break
is a guard nobody can prove.
"""

from __future__ import annotations

import datetime
import os
import sys

from content import KINDS, is_free, load, load_brands
from slug import RESERVED, VALID, slugify

REQUIRED = ("title", "brand", "source")
OPTIONAL = ("mount", "fixed_lens", "discontinued", "aliases", "note", "variant",
            "resources", "iso", "process", "film_type", "formats")

# Facts about an emulsion, and only about an emulsion: a camera has no ISO of
# its own and a lens has no development process, so these are refused elsewhere
# the same way `discontinued` is.
FILM_FIELDS = ("iso", "process", "film_type", "formats")

# `film_type` rather than `type` because Hugo owns `type` in front matter and
# uses it to pick a layout: `type = "Print"` would send every print film looking
# for `layouts/Print/`, and the failure would be a missing template rather than
# anything mentioning this field.
#
# Two values, because the source column has two. It distinguishes a negative
# that gets printed from a reversal that gets projected, which is the one thing
# about a film that changes what you can do with the result.
FILM_TYPES = ("Print", "Slide")
# What every photograph has to carry, and why each one.
IMAGE_PARAMS = {
    # Most of these licences require credit by name. A site-wide "images from
    # Wikimedia Commons" line does not satisfy CC BY, so the credit travels with
    # the file and is rendered beside it.
    "credit": "who took it, as the licence requires it be given",
    "license": "the licence, in the words the source uses",
    "licenseUrl": "where those words are defined",
    # A reader who cannot see the photograph still gets to know what it shows.
    "alt": "what the photograph shows",
    # The file page, not the article: the licence and the author live there, and
    # it is what a reuser has to be able to reach.
    "sourcePage": "the file's own page at the source",
    # When someone last confirmed the sentence above is still true. Every other
    # field describes the day the image arrived; this one is the only thing that
    # can go out of date on its own, without a commit, while the file sits here
    # looking checked.
    "verified": "the date someone last confirmed the source still says this",
}

# A photograph of a film box is the one thing here that no free licence can
# reach, and the reason is structural rather than a gap in Commons. A box is a
# graphic work and it is the whole subject of the picture, so a photograph of
# one has two copyright holders: whoever pressed the shutter and whoever drew
# the box. A contributor who shoots their own and offers it CC BY-SA is offering
# a licence to half of what is in the frame — which is why the free-licensed
# snapshot is the *unsafe* one here and the manufacturer's own product shot,
# where one owner holds both halves, is not. A sample of 120 of the 980 films
# found one with a box photograph on Commons at all.
#
# So `fair-use` is admitted, and it is admitted as what it is: a use, not a
# licence. It cannot be sublicensed, the corpus's CC BY-SA 4.0 does not reach
# it, and a reuser of this data does not inherit it. `licenseUrl` is meaningless
# for one — there are no terms to link — so it is replaced by the name of the
# holder, which is what makes the claim checkable rather than decorative.
# How long a claim may go unconfirmed before this refuses to pass it.
#
# It is a gate rather than a warning because the failure mode it exists for is
# nobody looking. A `sourcePage` is a URL and it will die: Silberra's domain
# already redirects somewhere unrelated, and Commons deletes files — routinely,
# and for the licensing reasons this whole scheme is about. A deleted Commons
# file leaves a photograph here whose credit Commons itself has withdrawn, and
# nothing in the repository would say so.
#
# So this will one day turn a pull request red for a reason that has nothing to
# do with it. That is the intended cost: the alternative is a repository full of
# claims nobody has checked since the day they were made, which is the state
# every one-shot importer leaves behind. The remedy is to re-check the sources
# and move the dates — not to raise the number because it went off.
STALE_AFTER_DAYS = 550          # about eighteen months
NON_FREE = "fair-use"
NON_FREE_PARAMS = {
    "copyright": "who owns the photograph and the packaging in it",
}
MOUNT_KEYS = ("title", "brand", "spellings", "note")
BRAND_KEYS = ("title", "brand", "aliases", "note")


def validate(root: str) -> list[str]:
    records, mounts, problems = load(root)
    problems = list(problems)

    def bad(where, msg):
        problems.append(f"{where}: {msg}")

    # --- mounts, first: everything else resolves against them ---------------
    spelling_owner: dict[str, str] = {}
    for term, meta in sorted(mounts.items()):
        rel = f"content/mount/{term}/_index.md"
        if not VALID.match(term):
            bad(rel, f"{term!r} is not a slug")
        if not meta.get("title"):
            bad(rel, "no title")
        for k in meta:
            if k not in MOUNT_KEYS:
                bad(rel, f"unknown field {k!r}")
        # A brand is optional here, and that is the point: M42 is a thread, not
        # a product, so no maker owns it and its URL carries no brand segment.
        for sp in meta.get("spellings", []):
            # Two mounts claiming one spelling makes the join between a body and
            # its glass ambiguous in exactly the way a mount record prevents.
            if sp in spelling_owner:
                bad(rel, f"spelling {sp!r} is already claimed by {spelling_owner[sp]}")
            spelling_owner[sp] = term

    # --- brands -------------------------------------------------------------
    brands, brand_broken = load_brands(root)
    problems.extend(brand_broken)
    brand_claimed: dict[tuple[str, str], str] = {k: f"content/{k[0]}/{k[1]}/_index.md"
                                                 for k in brands}
    for (kind, brand_slug), meta in sorted(brands.items()):
        rel = f"content/{kind}/{brand_slug}/_index.md"
        for f in meta:
            if f not in BRAND_KEYS:
                bad(rel, f"unknown field {f!r}")
        title = meta.get("title")
        if not isinstance(title, str) or not title.strip():
            bad(rel, "title is required and must be a non-empty string")
        elif slugify(title) != brand_slug:
            bad(rel, f"title {title!r} slugs to {slugify(title)!r}, not {brand_slug!r}. "
                     "A brand whose other names differ from its own carries them in "
                     "`aliases`, not in its title.")
        for alias in meta.get("aliases", []):
            if not isinstance(alias, str):
                bad(rel, f"alias {alias!r} is not a path")
                continue
            parts = alias.strip("/").split("/")
            if len(parts) != 2 or not alias.startswith("/"):
                bad(rel, f"alias {alias!r} is not /<kind>/<brand>/")
                continue
            akind, abrand = parts
            if akind != kind:
                bad(rel, f"alias {alias!r} is filed under {akind!r}, not {kind!r}")
                continue
            if not VALID.match(abrand):
                bad(rel, f"alias {alias!r} has a segment that is not a slug")
                continue
            key = (kind, abrand)
            if key in brands:
                # An alias redirects; one that shadows a real brand would send a
                # shelf away from itself.
                bad(rel, f"alias {alias!r} is already a brand")
            elif key in brand_claimed and brand_claimed[key] != rel:
                bad(rel, f"alias {alias!r} is also claimed by {brand_claimed[key]}")
            else:
                brand_claimed[key] = rel

    # --- records ------------------------------------------------------------
    canonical = {(r.kind, r.brand_slug, r.slug): r for r in records}
    claimed = {k: r.path for k, r in canonical.items()}

    for r in records:
        rel = r.path
        if not VALID.match(r.brand_slug):
            bad(rel, f"brand directory {r.brand_slug!r} is not a slug")
        if r.brand_slug in RESERVED:
            bad(rel, f"brand {r.brand_slug!r} collides with a path the site already answers")
        if not VALID.match(r.slug):
            bad(rel, f"{r.slug!r} is not a slug")
        for f in REQUIRED:
            if not isinstance(r.meta.get(f), str) or not r.meta[f].strip():
                bad(rel, f"{f} is required and must be a non-empty string")
        for f in r.meta:
            if f not in REQUIRED + OPTIONAL:
                bad(rel, f"unknown field {f!r}")
        # The directory *is* the brand. A record whose brand says one thing and
        # whose path says another has two answers to "who sold this", and the
        # URL is the one people will use.
        brand = r.meta.get("brand")
        if isinstance(brand, str) and slugify(brand) != r.brand_slug:
            bad(rel, f"brand {brand!r} slugs to {slugify(brand)!r}, not {r.brand_slug!r}")
        # The bundle's name is the stored slug: computed once, then frozen, so
        # correcting a title does not silently move a public URL. It must still
        # be *derivable* from the title — with the brand prefix dropped where the
        # title repeats it — or nothing connects the address to the thing.
        title = r.meta.get("title")
        variant = r.meta.get("variant")
        if variant is not None and (not isinstance(variant, str) or not variant.strip()):
            bad(rel, "variant must be a non-empty string")
            variant = None
        if isinstance(title, str):
            # A variant is an edition of a product, so two records can share a
            # title and be told apart by it — which means the slug has to carry
            # it, or they would share an address as well.
            names = [title] + ([f"{title} {variant}"] if variant else [])
            ok = set()
            for n in names:
                full = slugify(n)
                ok.add(full)
                if full.startswith(r.brand_slug + "-"):
                    ok.add(full[len(r.brand_slug) + 1:])
            if r.slug not in ok:
                bad(rel, f"slug {r.slug!r} is none of {sorted(ok)}")
            if variant and r.slug not in ok - {slugify(title),
                                               slugify(title)[len(r.brand_slug)+1:]}:
                bad(rel, f"slug {r.slug!r} does not carry the variant {variant!r}, so "
                         "another edition of this title would want the same address")
        if not str(r.meta.get("source", "")).startswith("https://"):
            bad(rel, "source must be an https URL")
        mount = r.meta.get("mount")
        if mount is not None:
            if not isinstance(mount, list) or not all(isinstance(m, str) for m in mount):
                bad(rel, "mount is a list of mount slugs")
            else:
                for m in mount:
                    if m not in mounts:
                        bad(rel, f"mount {m!r} has no term page in content/mount/")
        if r.kind == "film" and not isinstance(r.meta.get("discontinued"), bool):
            bad(rel, "a film says whether it is discontinued")
        if r.kind != "film" and "discontinued" in r.meta:
            bad(rel, "discontinued belongs to a film")
        for f in FILM_FIELDS:
            if r.kind != "film" and f in r.meta:
                bad(rel, f"{f} belongs to a film")
        # ISO is an integer so it can be compared and sorted. Roughly one film
        # in fifty carries two ratings in one cell ("40/50" — different markets,
        # or a change mid-life); those are left absent rather than flattened to
        # one number or stored as a string nothing can order.
        iso = r.meta.get("iso")
        if iso is not None and (not isinstance(iso, int) or isinstance(iso, bool)
                                or iso <= 0):
            bad(rel, "iso is a positive whole number, or absent")
        proc = r.meta.get("process")
        if proc is not None and (not isinstance(proc, str) or not proc.strip()):
            bad(rel, "process must be a non-empty string")
        ft = r.meta.get("film_type")
        if ft is not None and ft not in FILM_TYPES:
            bad(rel, f"film_type is one of {FILM_TYPES}, not {ft!r}")
        fmts = r.meta.get("formats")
        if fmts is not None:
            if (not isinstance(fmts, list) or not fmts
                    or not all(isinstance(x, str) and x.strip() for x in fmts)):
                bad(rel, "formats is a non-empty list of non-empty strings")
            elif len(set(fmts)) != len(fmts):
                bad(rel, "formats repeats a format")
        # A body takes a mount or has a lens built into it, never both: the two
        # infobox fields these came from answer one question between them.
        if mount and r.meta.get("fixed_lens"):
            bad(rel, "claims both a mount and a fixed lens")

    # --- photographs --------------------------------------------------------
    # An image is the one thing here that can put someone in breach of a licence
    # by being committed, so this refuses rather than warns.
    today = datetime.date.today()
    stale: list[tuple[str, str, str, int]] = []
    for r in records:
        declared = {}
        for res in r.meta.get("resources", []):
            if not isinstance(res, dict) or not isinstance(res.get("src"), str):
                bad(r.path, f"resource {res!r} needs a src")
                continue
            declared[res["src"]] = res.get("params") or {}
        for src in declared:
            if src not in r.images:
                bad(r.path, f"resources names {src!r}, which is not in the bundle")
        for img in r.images:
            params = declared.get(img)
            if params is None:
                bad(r.path, f"{img} has no [[resources]] entry, so it ships with no "
                            "credit and no licence")
                continue
            lic = str(params.get("license", "")).strip().lower()
            # A fair-use file has no terms to link, so it answers for itself with
            # the holder's name instead of a licenceUrl. Everything else still
            # has to be a licence this repository can actually redistribute.
            wanted = dict(IMAGE_PARAMS)
            if lic == NON_FREE:
                del wanted["licenseUrl"]
                wanted.update(NON_FREE_PARAMS)
            for field, why in sorted(wanted.items()):
                if not str(params.get(field, "")).strip():
                    bad(r.path, f"{img} has no {field} — {why}")
            for field in set(IMAGE_PARAMS) | set(NON_FREE_PARAMS):
                if field not in wanted and str(params.get(field, "")).strip():
                    bad(r.path, f"{img} is {lic} and carries a {field}, which says "
                                f"nothing true about it")
            if lic and lic != NON_FREE and not is_free(lic):
                bad(r.path, f"{img} is licensed {params['license']!r}, which is not a "
                            "licence this repository can redistribute under. A "
                            "fair-use file looks exactly like a free one from the "
                            "article side; check the file page.")
            if not str(params.get("sourcePage", "")).startswith("https://"):
                bad(r.path, f"{img} sourcePage must be an https URL to the file's own page")
            checked = str(params.get("verified", "")).strip()
            if checked:
                try:
                    when = datetime.date.fromisoformat(checked)
                except ValueError:
                    bad(r.path, f"{img} verified {checked!r} is not a date (YYYY-MM-DD)")
                else:
                    if when > today:
                        bad(r.path, f"{img} was verified on {checked}, which has not happened")
                    elif (today - when).days > STALE_AFTER_DAYS:
                        stale.append((r.path, img, checked, (today - when).days))

    # Reported as one group rather than one problem per file: the answer is to
    # go re-check a batch of sources, and a hundred separate lines would bury
    # every other thing this found.
    if stale:
        oldest = max(days for _, _, _, days in stale)
        problems.append(
            f"{len(stale)} image claim(s) have not been re-verified in over "
            f"{STALE_AFTER_DAYS} days, the oldest by {oldest - STALE_AFTER_DAYS}. "
            f"Re-check the sources still say what the credit says, then move the "
            f"`verified` dates. First few: "
            + "; ".join(f"{path} {img} ({when})" for path, img, when, _ in stale[:3]))

    # --- aliases ------------------------------------------------------------
    # Hugo's own field, so Hugo generates the redirect page and nothing here has
    # to. The path is root-relative *within* the site: Hugo prepends baseURL's
    # own prefix, which is why `/library` does not appear in one.
    for r in records:
        for alias in r.meta.get("aliases", []):
            if not isinstance(alias, str):
                bad(r.path, f"alias {alias!r} is not a path")
                continue
            parts = alias.strip("/").split("/")
            if len(parts) != 3 or not alias.startswith("/"):
                bad(r.path, f"alias {alias!r} is not /<kind>/<brand>/<slug>/")
                continue
            kind, brand, slug = parts
            if kind != r.kind:
                # A camera reached at a lens address would be a redirect across
                # two things that are not the same kind of thing.
                bad(r.path, f"alias {alias!r} is filed under {kind!r}, not {r.kind!r}")
                continue
            if not (VALID.match(brand) and VALID.match(slug)):
                bad(r.path, f"alias {alias!r} has a segment that is not a slug")
                continue
            key = (kind, brand, slug)
            if key in canonical:
                # An alias redirects. One that shadows a real record would
                # redirect a page away from itself.
                bad(r.path, f"alias {alias!r} is already a record")
            elif key in claimed and claimed[key] != r.path:
                bad(r.path, f"alias {alias!r} is also claimed by {claimed[key]}")
            else:
                claimed[key] = r.path
    return problems


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = validate(root)
    for p in problems:
        print(p)
    records, mounts, _ = load(root)
    if problems:
        print(f"\n{len(problems)} problem(s)")
        return 1
    promoted = sum(1 for r in records if r.promoted)
    by_kind = {k: sum(1 for r in records if r.kind == k) for k in KINDS}
    print(f"{len(records)} records {by_kind}, {len(mounts)} mounts, no problems")
    print(f"{promoted} have earned a page of their own; "
          f"{len(records) - promoted} redirect to their brand list")
    # Printed on every green run, because the number quietly growing is the
    # thing this is about and a gate that only speaks when it fires teaches
    # nobody anything before it does.
    ages = []
    for r in records:
        for res in r.meta.get("resources", []):
            when = str((res.get("params") or {}).get("verified", "")).strip()
            try:
                ages.append((datetime.date.today() - datetime.date.fromisoformat(when)).days)
            except ValueError:
                pass
    if ages:
        print(f"{len(ages)} image claim(s), oldest verified {max(ages)} days ago, "
              f"stale at {STALE_AFTER_DAYS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
