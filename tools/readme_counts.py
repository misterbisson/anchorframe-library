"""The numbers in README.md, computed from the corpus rather than typed.

Every count of this repository in that file goes stale, because every pull
request changes one. Between #8 and #28 four of them drifted — lenses by 23,
film brands by 5, film photographs from five to seventy — and the sentence
saying the corpus holds no film detail stayed there through the two releases
that added it.

So the counts live in a generated block and this asserts the block is current.
It is a check rather than a formatter for the same reason `check_stubs.py` is:
a number nobody verifies is a claim, and a claim in a README is the first thing
a reader trusts.

    python3 tools/readme_counts.py            # fail if the block is stale
    python3 tools/readme_counts.py --write    # bring it up to date

**A count of this corpus is generated. A measurement of the world is dated.**
That 201 of 341 camera articles carry a lead image is a fact about Wikipedia on
the day someone looked, and regenerating it would mean re-crawling; it stays in
prose with the date it was taken. Everything a `load()` can answer belongs here.
"""

from __future__ import annotations

import os
import sys

from content import load, load_brands

START = "<!-- counts:start -->"
END = "<!-- counts:end -->"
KINDS = (("camera", "cameras"), ("lens", "lenses"), ("film", "films"))


def counts(root: str) -> dict:
    records, mounts, _ = load(root)
    brands, _ = load_brands(root)
    films = [r for r in records if r.kind == "film"]
    out = {
        "kinds": [
            {
                "label": label,
                "records": sum(1 for r in records if r.kind == kind),
                "brands": sum(1 for (k, _) in brands if k == kind),
                "photographs": sum(1 for r in records if r.kind == kind and r.images),
            }
            for kind, label in KINDS
        ],
        "mounts": len(mounts),
        "in_production": sum(1 for r in films if not r.meta.get("discontinued")),
        "discontinued": sum(1 for r in films if r.meta.get("discontinued")),
        "films": len(films),
    }
    for field in ("iso", "process", "formats", "types"):
        out[field] = sum(1 for r in films if field in r.meta)
    # How a body takes its glass, three ways. The third is the one worth
    # counting: a camera naming neither is not a camera with no mount, it is a
    # camera nobody has asked. Those two were one number until they were split.
    cameras = [r for r in records if r.kind == "camera"]
    out["cameras"] = len(cameras)
    out["with_mount"] = sum(1 for r in cameras if r.meta.get("mount"))
    out["integrated"] = sum(1 for r in cameras if r.meta.get("integrated"))
    out["with_fixed"] = sum(1 for r in cameras if r.meta.get("fixed_lens"))
    out["lens_silent"] = (out["cameras"] - out["with_mount"] - out["integrated"])
    return out


def render(c: dict) -> str:
    rows = "\n".join(
        f"| {k['label']} | {k['records']:,} | {k['brands']} | {k['photographs']} |"
        for k in c["kinds"]
    )
    return f"""{START}
| | records | brands | with a photograph |
| --- | --- | --- | --- |
{rows}
| mounts | {c['mounts']} | — | — |

Of the {c['cameras']} cameras, {c['with_mount']} name the mount they take and
{c['integrated']} have a lens that does not come off — {c['with_fixed']} of
those also name the glass. **{c['lens_silent']} say neither**, which is not the
same as having nothing to say: absent is how this corpus writes both "has no
mount" and "nobody has looked", and only one of those is a fact.

Of the {c['films']:,} films, **{c['in_production']} are still in production**.
What the two source articles say about them: speed on {c['iso']}, process on
{c['process']}, format on {c['formats']}, and print-or-slide on {c['types']} —
each one a term you can browse by.
{END}"""


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "README.md")
    text = open(path, encoding="utf-8").read()
    if START not in text or END not in text:
        print(f"README.md has no {START} … {END} block to keep current")
        return 1
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    fresh = render(counts(root))
    current = START + rest.split(END, 1)[0] + END
    if current == fresh:
        print("README counts are current")
        return 0
    if "--write" in sys.argv:
        open(path, "w", encoding="utf-8").write(head + fresh + tail)
        print("README counts brought up to date")
        return 0
    print("README.md counts are stale. Run: python3 tools/readme_counts.py --write\n")
    for a, b in zip(current.split("\n"), fresh.split("\n")):
        if a != b:
            print(f"  says: {a}\n  is:   {b}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
