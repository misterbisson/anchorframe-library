"""The check that stands between a pull request and the data.

The extraction that seeded this repository is not something anyone re-runs on a
schedule: it took judgement, and reproducing it would take more. So the files in
`data/` are the source of truth rather than an output, they are edited by hand,
and this is what makes a hand edit safe to accept by reading its diff instead of
the whole corpus.

Every rule here is mutation-tested in `test_validate.py`: a guard that no test
can break is a guard nobody can prove.
"""

from __future__ import annotations

import json
import os
import sys

from slug import RESERVED, VALID, slugify

KINDS = ("camera", "film", "lens")
REQUIRED = ("name", "brand", "source")
OPTIONAL = ("mount", "lens", "discontinued", "alternates", "note")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate(root: str) -> list[str]:
    problems: list[str] = []
    def bad(where, msg): problems.append(f"{where}: {msg}")

    # --- mounts, first: everything else resolves against them ---------------
    mounts, spelling_owner = {}, {}
    mount_dir = os.path.join(root, "data", "mount")
    for fn in sorted(os.listdir(mount_dir)) if os.path.isdir(mount_dir) else []:
        if not fn.endswith(".json"):
            continue
        key, rel = fn[:-5], f"data/mount/{fn}"
        if not VALID.match(key):
            bad(rel, f"{key!r} is not a slug")
        rec = _load(os.path.join(mount_dir, fn))
        mounts[key] = rec
        if not rec.get("name"):
            bad(rel, "no name")
        # A brand is optional here and that is the point: M42 is a thread, not a
        # product, so no maker owns it and its URL carries no brand segment.
        for sp in rec.get("spellings", []):
            # Two mounts claiming one spelling makes the join ambiguous in
            # exactly the way a mount record exists to prevent.
            if sp in spelling_owner:
                bad(rel, f"spelling {sp!r} is already claimed by {spelling_owner[sp]}")
            spelling_owner[sp] = key

    # --- records ------------------------------------------------------------
    canonical: dict[tuple[str, str, str], str] = {}
    claimed: dict[tuple[str, str, str], str] = {}
    for kind in KINDS:
        kdir = os.path.join(root, "data", kind)
        if not os.path.isdir(kdir):
            bad(f"data/{kind}", "missing")
            continue
        for brand_slug in sorted(os.listdir(kdir)):
            bdir = os.path.join(kdir, brand_slug)
            if not os.path.isdir(bdir):
                continue
            if not VALID.match(brand_slug):
                bad(f"data/{kind}/{brand_slug}", "brand directory is not a slug")
            if brand_slug in RESERVED:
                bad(f"data/{kind}/{brand_slug}", "brand collides with a path the site already answers")
            for fn in sorted(os.listdir(bdir)):
                rel = f"data/{kind}/{brand_slug}/{fn}"
                if not fn.endswith(".json"):
                    bad(rel, "not a .json file")
                    continue
                s = fn[:-5]
                if not VALID.match(s):
                    bad(rel, f"{s!r} is not a slug")
                rec = _load(os.path.join(bdir, fn))
                for f in REQUIRED:
                    if not isinstance(rec.get(f), str) or not rec[f].strip():
                        bad(rel, f"{f} is required and must be a non-empty string")
                for f in rec:
                    if f not in REQUIRED + OPTIONAL:
                        bad(rel, f"unknown field {f!r}")
                # The directory *is* the brand. A record whose brand says one
                # thing and whose path says another has two answers to "who sold
                # this", and the URL is the one people will use.
                if isinstance(rec.get("brand"), str) and slugify(rec["brand"]) != brand_slug:
                    bad(rel, f"brand {rec['brand']!r} slugs to "
                             f"{slugify(rec['brand'])!r}, not {brand_slug!r}")
                # The filename is the stored slug: computed once, then frozen, so
                # correcting a name does not silently move a public URL. It must
                # still be *derivable* from the name — with the brand prefix
                # dropped where the name repeats it — or nothing connects the two.
                if isinstance(rec.get("name"), str):
                    full = slugify(rec["name"])
                    trimmed = full[len(brand_slug) + 1:] if full.startswith(brand_slug + "-") else full
                    if s not in (full, trimmed):
                        bad(rel, f"slug {s!r} is neither {full!r} nor {trimmed!r}")
                if not str(rec.get("source", "")).startswith("https://"):
                    bad(rel, "source must be an https URL")
                m = rec.get("mount")
                if m is not None and m not in mounts:
                    bad(rel, f"mount {m!r} has no record in data/mount/")
                if kind == "film" and not isinstance(rec.get("discontinued"), bool):
                    bad(rel, "a film says whether it is discontinued")
                if kind != "film" and "discontinued" in rec:
                    bad(rel, "discontinued belongs to a film")
                # A body takes a mount or has a lens built into it, never both:
                # the two infobox fields answer one question between them.
                if rec.get("mount") and rec.get("lens"):
                    bad(rel, "claims both a mount and a fixed lens")
                key = (kind, brand_slug, s)
                canonical[key] = rel
                claimed[key] = rel

    # --- alternates ---------------------------------------------------------
    for (kind, brand_slug, s), rel in sorted(canonical.items()):
        rec = _load(os.path.join(root, rel))
        for alt in rec.get("alternates", []):
            if not isinstance(alt, dict) or set(alt) != {"brand", "slug"}:
                bad(rel, f"alternate {alt!r} needs exactly a brand and a slug")
                continue
            if not (VALID.match(alt["brand"]) and VALID.match(alt["slug"])):
                bad(rel, f"alternate {alt['brand']}/{alt['slug']} is not a slug pair")
                continue
            key = (kind, alt["brand"], alt["slug"])
            if key in canonical:
                # An alternate redirects. One that shadows a real record would
                # redirect a page away from itself.
                bad(rel, f"alternate {alt['brand']}/{alt['slug']} is already a record")
            elif key in claimed and claimed[key] != rel:
                bad(rel, f"alternate {alt['brand']}/{alt['slug']} is also claimed by {claimed[key]}")
            else:
                claimed[key] = rel
    return problems


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = validate(root)
    for p in problems:
        print(p)
    n = sum(len(files) for _, _, files in os.walk(os.path.join(root, "data")))
    if problems:
        print(f"\n{len(problems)} problem(s) across {n} files")
        return 1
    print(f"{n} files, no problems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
