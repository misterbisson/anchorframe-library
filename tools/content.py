"""Reading the corpus: one leaf bundle per thing.

Every record is `content/<kind>/<brand>/<slug>/index.md` — a Hugo **leaf
bundle**, which is a directory even when it holds one file. That is deliberate
and it is not about storage: a directory sitting beside a record is an
invitation to drop a photograph into it, and a bare `<slug>.md` is not. Since
promotion from flat file to bundle would be as disruptive as the move to
markdown was, everything starts as a bundle.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field

KINDS = ("camera", "film", "lens")
FRONT = "+++"
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".tif", ".tiff")


@dataclass
class Record:
    kind: str
    brand_slug: str
    slug: str
    path: str                       # repo-relative, for error messages
    meta: dict
    body: str
    images: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"/library/{self.kind}/{self.brand_slug}/{self.slug}"

    @property
    def promoted(self) -> bool:
        """Whether this thing has earned a page of its own.

        Most records are a name, a brand and a link, and a page of that is a
        page that exists in order not to be a 404. A record crosses the line by
        having something to show — prose, or a photograph — and the moment it
        does, its page appears at the address it always had. Nothing is renamed
        and no redirect has to be withdrawn by hand, because the threshold is
        computed from the content rather than recorded next to it.
        """
        return bool(self.body.strip()) or bool(self.images)


def parse_front_matter(text: str, path: str) -> tuple[dict, str]:
    if not text.startswith(FRONT):
        raise ValueError(f"{path}: no TOML front matter (a file starts with +++)")
    end = text.find("\n" + FRONT, len(FRONT))
    if end < 0:
        raise ValueError(f"{path}: front matter is never closed")
    head = text[len(FRONT):end]
    body = text[end + len(FRONT) + 1:]
    try:
        meta = tomllib.loads(head)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"{path}: front matter is not valid TOML — {e}") from e
    return meta, body


def load(root: str) -> tuple[list[Record], dict[str, dict], list[str]]:
    """Records, mount terms, and any file that could not be read at all."""
    records: list[Record] = []
    mounts: dict[str, dict] = {}
    broken: list[str] = []

    def read(path, rel):
        with open(path, encoding="utf-8") as fh:
            return parse_front_matter(fh.read(), rel)

    for kind in KINDS:
        base = os.path.join(root, "content", kind)
        if not os.path.isdir(base):
            broken.append(f"content/{kind}: missing")
            continue
        for brand_slug in sorted(os.listdir(base)):
            bdir = os.path.join(base, brand_slug)
            if not os.path.isdir(bdir):
                # `_index.md` for the kind itself is a list page, not a record.
                if brand_slug != "_index.md":
                    broken.append(f"content/{kind}/{brand_slug}: not a brand directory")
                continue
            for slug in sorted(os.listdir(bdir)):
                sdir = os.path.join(bdir, slug)
                rel = f"content/{kind}/{brand_slug}/{slug}"
                if not os.path.isdir(sdir):
                    if slug != "_index.md":
                        broken.append(f"{rel}: every record is a leaf bundle "
                                      f"(a directory holding index.md), never a bare file")
                    continue
                page = os.path.join(sdir, "index.md")
                if not os.path.isfile(page):
                    broken.append(f"{rel}: bundle has no index.md")
                    continue
                try:
                    meta, body = read(page, f"{rel}/index.md")
                except ValueError as e:
                    broken.append(str(e))
                    continue
                images = sorted(f for f in os.listdir(sdir)
                                if f.lower().endswith(IMAGE_SUFFIXES))
                records.append(Record(kind, brand_slug, slug, f"{rel}/index.md",
                                      meta, body, images))

    mdir = os.path.join(root, "content", "mount")
    for term in sorted(os.listdir(mdir)) if os.path.isdir(mdir) else []:
        tdir = os.path.join(mdir, term)
        if not os.path.isdir(tdir):
            continue
        page = os.path.join(tdir, "_index.md")
        rel = f"content/mount/{term}/_index.md"
        if not os.path.isfile(page):
            broken.append(f"content/mount/{term}: no _index.md")
            continue
        try:
            meta, _ = read(page, rel)
        except ValueError as e:
            broken.append(str(e))
            continue
        mounts[term] = meta
    return records, mounts, broken
