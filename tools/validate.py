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

import os
import sys

from content import KINDS, load
from slug import RESERVED, VALID, slugify

REQUIRED = ("title", "brand", "source")
OPTIONAL = ("mount", "fixed_lens", "discontinued", "alternates", "note")
MOUNT_KEYS = ("title", "brand", "spellings", "note")


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
        if isinstance(title, str):
            full = slugify(title)
            trimmed = (full[len(r.brand_slug) + 1:]
                       if full.startswith(r.brand_slug + "-") else full)
            if r.slug not in (full, trimmed):
                bad(rel, f"slug {r.slug!r} is neither {full!r} nor {trimmed!r}")
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
        # A body takes a mount or has a lens built into it, never both: the two
        # infobox fields these came from answer one question between them.
        if mount and r.meta.get("fixed_lens"):
            bad(rel, "claims both a mount and a fixed lens")

    # --- alternates ---------------------------------------------------------
    for r in records:
        for alt in r.meta.get("alternates", []):
            if not isinstance(alt, dict) or set(alt) != {"brand", "slug"}:
                bad(r.path, f"alternate {alt!r} needs exactly a brand and a slug")
                continue
            if not (VALID.match(str(alt["brand"])) and VALID.match(str(alt["slug"]))):
                bad(r.path, f"alternate {alt['brand']}/{alt['slug']} is not a slug pair")
                continue
            key = (r.kind, alt["brand"], alt["slug"])
            if key in canonical:
                # An alternate redirects. One that shadows a real record would
                # redirect a page away from itself.
                bad(r.path, f"alternate {alt['brand']}/{alt['slug']} is already a record")
            elif key in claimed and claimed[key] != r.path:
                bad(r.path, f"alternate {alt['brand']}/{alt['slug']} is also claimed by {claimed[key]}")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
