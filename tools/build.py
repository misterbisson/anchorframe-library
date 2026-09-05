"""`content/` -> `dist/`: sheets for the app, and the redirect manifest for the site.

`dist/` is not committed. The bundles are the source of truth, so a built copy in
the tree would be a second answer to the same question, and a stale one the first
time someone forgets to rebuild.
"""

from __future__ import annotations

import datetime
import json
import os
import sys

from content import KINDS, load, url_prefix
from validate import validate

LICENSE = "CC-BY-SA-4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
ATTRIBUTION = (
    "Equipment names extracted from English Wikipedia and used under CC BY-SA 4.0, "
    "with corrections and additions contributed to "
    "https://github.com/misterbisson/anchorframe-library. Each entry carries the "
    "source it was read from."
)


def _stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sheets(root: str) -> dict[str, dict]:
    records, mounts, _ = load(root)
    stamp = _stamp()
    out: dict[str, dict] = {}
    for kind in KINDS:
        entries = []
        for r in (x for x in records if x.kind == kind):
            e = {"name": r.meta["title"], "brand": r.meta["brand"], "slug": r.slug,
                 "url": r.url, "source": r.meta["source"], "promoted": r.promoted}
            if r.meta.get("mount"):
                e["mount"] = r.meta["mount"][0]
            for k in ("fixed_lens", "discontinued", "note", "aliases"):
                if k in r.meta:
                    e[k] = r.meta[k]
            entries.append(e)
        entries.sort(key=lambda e: (e["brand"].casefold(), e["slug"]))
        out[kind] = {"license": LICENSE, "licenseUrl": LICENSE_URL,
                     "attribution": ATTRIBUTION, "generated": stamp, "entries": entries}
    out["mount"] = {
        "license": LICENSE, "licenseUrl": LICENSE_URL, "attribution": ATTRIBUTION,
        "generated": stamp,
        "entries": sorted(
            ({"slug": t, "url": f"{url_prefix(root)}/mount/{t}", **m}
             for t, m in mounts.items()),
            key=lambda e: e["slug"]),
    }
    return out


def redirects(root: str) -> dict:
    """Every address that answers with a 301, and where it points.

    Two kinds, and they have different lifetimes. An **alternate** is permanent:
    one product with two names, and the name that is not the address will never
    become one. A **thin** record's redirect is provisional by design — it lasts
    exactly as long as the record has nothing to show, and disappears on its own
    the day someone drops a photograph into the bundle. So the second set is
    computed here on every build rather than maintained by hand, and a consumer
    should cache it briefly rather than forever.
    """
    records, _, _ = load(root)
    thin, alt = [], []
    for r in records:
        if not r.promoted:
            # The path was always the address, so promoting a record is deleting
            # a redirect: no link breaks, because nothing moves.
            thin.append({"from": r.url, "to": r.list_url})
        for a in r.meta.get("aliases", []):
            # Hugo prepends baseURL's prefix to an alias; this manifest states
            # the address as served, so it does the same.
            alt.append({"from": f"{r.prefix}{a.rstrip('/')}", "to": r.url})
    thin.sort(key=lambda x: x["from"])
    alt.sort(key=lambda x: x["from"])
    return {"generated": _stamp(), "permanent": alt, "provisional": thin}


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = validate(root)
    if problems:
        # Building over a corpus that does not validate produces a plausible
        # set of sheets rather than an obviously broken one, which is worse.
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s); not building")
        return 1
    dist = os.path.join(root, "dist")
    os.makedirs(dist, exist_ok=True)
    for kind, sheet in sheets(root).items():
        with open(os.path.join(dist, f"{kind}.json"), "w", encoding="utf-8") as fh:
            json.dump(sheet, fh, indent=2, ensure_ascii=False, sort_keys=True)
            fh.write("\n")
        print(f"{len(sheet['entries']):5d} -> dist/{kind}.json")
    r = redirects(root)
    with open(os.path.join(dist, "redirects.json"), "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print(f"{len(r['permanent']):5d} permanent + {len(r['provisional'])} provisional "
          f"-> dist/redirects.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
