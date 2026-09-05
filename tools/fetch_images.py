"""Fetch a photograph for a record from Wikimedia Commons, with its credit.

Run on a person's machine, never in CI, and its output is committed — the same
shape as the extraction that seeded this repository.

**Two rules do the safety work here, and both are mechanical.**

Only files whose `imagerepository` is `shared` are taken. That means Commons.
English Wikipedia also stores files locally, and local is where non-free
fair-use uploads live; from the article side they look exactly like the other
199. Two of the 201 camera images are local, and no amount of reading the
article would tell you which.

Only licences `content.FREE_LICENCES` accepts are taken. Everything else is
skipped and printed, rather than downloaded and argued about later.

The credit is written into the record's front matter as Hugo `[[resources]]`
params, so `tools/validate.py` can refuse an image that arrives without one and
the page can render the attribution beside the photograph — which is what CC BY
actually requires, and what a single site-wide line would not satisfy.

    python3 tools/fetch_images.py --dry-run          # what it would take
    python3 tools/fetch_images.py --brand canon      # one shelf
    python3 tools/fetch_images.py                    # everything it can
"""

from __future__ import annotations

import argparse
import html
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from content import FREE_LICENCES, load

API = "https://en.wikipedia.org/w/api.php"
UA = ("anchorframe-library-image-fetch/1.0 "
      "(https://github.com/misterbisson/anchorframe-library)")
# Wide enough to stay useful, small enough that a few hundred do not bloat the
# repository. Hugo generates the served derivative from this, not the other way.
WIDTH = 1000


def get(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json", formatversion="2"))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - any failure is worth a retry here
            if attempt == 4:
                raise
            # Wikimedia's policy asks for this and enforces it; the second run of
            # the original extractor was refused with HTTP 429 partway through.
            time.sleep(2 ** attempt)
    return {}


def strip_html(s: str) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
    # The Artist field renders as links, so stripping tags leaves their labels
    # behind: "SNx at English Wikipedia (log)". Those are file-page furniture,
    # not part of anybody's name.
    s = re.sub(r"\s*\((?:log|talk|page does not exist|contribs)\)", "", s, flags=re.I)
    return re.sub(r"\s+", " ", s).strip(" ·,;")


def download(url: str, path: str) -> None:
    """Fetch one file, politely.

    The API calls back off and the downloads did not, which is how the first
    real run was cut off with HTTP 429 after ten images. Wikimedia asks for this
    and enforces it; the original extraction learned the same lesson.
    """
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            with open(path, "wb") as fh:
                fh.write(data)
            return
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 5:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 5 * (2 ** attempt)
            print(f"        {e.code}; waiting {wait}s")
            time.sleep(wait)
        except Exception:
            if attempt == 5:
                raise
            time.sleep(5 * (2 ** attempt))


def article_of(record) -> str | None:
    """The article a record was read from, if it has one of its own."""
    src = record.meta["source"]
    if "#" in src:                      # a row in a list article, not its own page
        return None
    return urllib.parse.unquote(src.split("/wiki/")[-1]).replace("_", " ")


def candidates(root: str, brand: str | None, kind: str):
    for r in load(root)[0]:
        if r.kind != kind or (brand and r.brand_slug != brand):
            continue
        if r.images or article_of(r) is None:
            continue
        yield r


def lead_images(titles: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i in range(0, len(titles), 40):
        d = get({"action": "query", "prop": "pageimages", "piprop": "name",
                 "titles": "|".join(titles[i:i + 40])})
        for p in d.get("query", {}).get("pages", []):
            name = (p.get("pageimage") or "").replace(" ", "_")
            if name:
                out[p["title"]] = name
        time.sleep(0.6)
    return out


def file_info(names: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i in range(0, len(names), 25):
        d = get({"action": "query", "prop": "imageinfo",
                 "iiprop": "extmetadata|url|size", "iiurlwidth": WIDTH,
                 "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|ImageDescription",
                 "titles": "|".join("File:" + n for n in names[i:i + 25])})
        for p in d.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata")
            em = em if isinstance(em, dict) else {}
            out[p["title"][5:].replace(" ", "_")] = {
                "repo": p.get("imagerepository"),
                "license": strip_html((em.get("LicenseShortName") or {}).get("value", "")),
                "licenseUrl": strip_html((em.get("LicenseUrl") or {}).get("value", "")),
                "credit": strip_html((em.get("Artist") or {}).get("value", "")),
                "desc": strip_html((em.get("ImageDescription") or {}).get("value", "")),
                "thumb": ii.get("thumburl"),
                "page": ii.get("descriptionurl"),
            }
        time.sleep(0.6)
    return out


def acceptable(info: dict) -> str | None:
    """Why this file cannot be used, or None if it can."""
    if info.get("repo") != "shared":
        return "not on Commons (a local upload may be non-free)"
    if not info.get("license"):
        return "no licence stated"
    if not info["license"].lower().startswith(FREE_LICENCES):
        return f"licence {info['license']!r} is not redistributable here"
    if not info.get("credit"):
        return "no author named, so the licence cannot be satisfied"
    if not info.get("thumb") or not info.get("page"):
        return "no file URL"
    return None


def attach(record, filename: str, info: dict, alt: str) -> None:
    path = os.path.join(os.path.dirname(record.path), filename)
    download(info["thumb"], path)
    def esc(v: str) -> str:
        return v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    block = (f'\n[[resources]]\nsrc = "{filename}"\n[resources.params]\n'
             f'credit = "{esc(info["credit"])}"\n'
             f'license = "{esc(info["license"])}"\n'
             f'licenseUrl = "{esc(info["licenseUrl"] or "https://commons.wikimedia.org/wiki/Commons:Licensing")}"\n'
             f'alt = "{esc(alt)}"\n'
             f'sourcePage = "{esc(info["page"])}"\n')
    s = io.open(record.path, encoding="utf-8").read()
    head, rest = s.split("+++\n", 1)[1].split("\n+++", 1)
    io.open(record.path, "w", encoding="utf-8").write("+++\n" + head + "\n" + block + "+++" + rest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--brand")
    ap.add_argument("--kind", default="camera")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    recs = list(candidates(root, args.brand, args.kind))
    if args.limit:
        recs = recs[:args.limit]
    print(f"{len(recs)} record(s) with an article of their own and no image yet")
    if not recs:
        return 0

    by_title = {article_of(r): r for r in recs}
    leads = lead_images(sorted(by_title))
    infos = file_info(sorted(set(leads.values())))

    taken = skipped = none = 0
    reasons: dict[str, int] = {}
    for title, rec in sorted(by_title.items()):
        name = leads.get(title)
        if not name:
            none += 1
            continue
        info = infos.get(name, {})
        why = acceptable(info)
        if why:
            skipped += 1
            reasons[why.split(" is not")[0][:48]] = reasons.get(why.split(" is not")[0][:48], 0) + 1
            print(f"  skip  {rec.url}\n        {why}")
            continue
        alt = info["desc"][:160] or f"{rec.meta['title']}, photographed"
        ext = os.path.splitext(name)[1].lower() or ".jpg"
        if args.dry_run:
            print(f"  take  {rec.url}\n        {info['license']} · {info['credit'][:52]}")
        else:
            attach(rec, f"{rec.slug}{ext}", info, alt)
            # A record that already has an image is skipped, so an interrupted
            # run resumes by being run again.
            time.sleep(1.5)
        taken += 1

    print(f"\n{'would take' if args.dry_run else 'took'}: {taken}   "
          f"skipped: {skipped}   no lead image: {none}")
    for why, n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        print(f"    {n:4d}  {why}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
