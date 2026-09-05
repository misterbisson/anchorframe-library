"""`data/` -> `dist/`: one sheet per kind, for the app and the site to read.

`dist/` is not committed. The records are the source of truth, so a built copy
in the tree would be a second answer to the same question, and a stale one the
first time someone forgets to rebuild.
"""

from __future__ import annotations

import datetime
import json
import os
import sys

from validate import KINDS, validate

LICENSE = "CC-BY-SA-4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
ATTRIBUTION = (
    "Equipment names extracted from English Wikipedia and used under CC BY-SA 4.0, "
    "with corrections and additions contributed to "
    "https://github.com/misterbisson/anchorframe-library. Each entry carries the "
    "source it was read from."
)


def sheets(root: str) -> dict[str, dict]:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {}
    for kind in KINDS + ("mount",):
        entries = []
        base = os.path.join(root, "data", kind)
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                if not fn.endswith(".json"):
                    continue
                with open(os.path.join(dirpath, fn), encoding="utf-8") as fh:
                    rec = json.load(fh)
                slug = fn[:-5]
                if kind == "mount":
                    rec["slug"] = slug
                    rec["url"] = f"/library/mount/{slug}"
                else:
                    brand_slug = os.path.basename(dirpath)
                    rec["slug"] = slug
                    rec["url"] = f"/library/{kind}/{brand_slug}/{slug}"
                entries.append(rec)
        entries.sort(key=lambda r: (r.get("brand", "").casefold(), r["slug"]))
        out[kind] = {
            "license": LICENSE, "licenseUrl": LICENSE_URL,
            "attribution": ATTRIBUTION, "generated": stamp, "entries": entries,
        }
    return out


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = validate(root)
    if problems:
        # Building over a corpus that does not validate produces a plausible
        # sheet rather than an obviously broken one, which is the worse failure.
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
